"""Joke-related request handlers.

The joke status workflow is as follows:

* Extracted
* Extraction-verified
* Auto-transcribed
* Transcribed
* Transcription-verified
* Auto-categorised
* Categories-verified
* Annotated
* Annotation-verified
* Published
"""
import logging
import math

from aiocouch import Document, exception as aio_exc
from aiocouch.attachment import Attachment
from base64 import b64encode
from datetime import datetime
from io import BytesIO
from PIL import Image
from typing import Union
from uuid import uuid1

from .base import JSONAPICollectionHandler, JSONAPIItemHandler, JSONAPIError
from toja.utils import couchdb, mosquitto
from toja.validation import validate, ValidationError, object_schema, type_schema, one_to_one_relationship_schema


logger = logging.getLogger(__name__)


def coerce_coordinates(value: list) -> list:
    """Coerce the coordinates into an integer bounding box."""
    if not value:
        return value
    if len(value) == 4:
        return [
            int(math.floor(value[0])),
            int(math.floor(value[1])),
            int(math.ceil(value[2])),
            int(math.ceil(value[3])),
        ]
    else:
        return []


async def as_jsonapi(doc: Document, user: Union[Document, None]) -> dict:
    """Return a single joke as JSONAPI."""
    async with couchdb() as session:
        db = await session['jokes']
        doc = await db[doc['_id']]
        image = Attachment(doc, 'image')
        image_data = f'data:image/png;base64,{b64encode(await image.fetch()).decode("utf-8")}'
    full_rights = 'admin' in user['groups'] or 'editor' in user['groups']
    return {
        'id': doc['_id'],
        'type': 'jokes',
        'attributes': {
            'title': doc['title'],
            'coordinates': doc['coordinates'],
            'transcriptions': doc['transcriptions']
                if full_rights else dict([(key, value)
                                          for key, value in doc['transcriptions'].items()
                                          if key in ['auto', 'verified', 'final',
                                                     user['_id'] if user else None]]),
            'categories': doc['categories'],
            'topics': doc['topics'] if 'topics' in doc else '',
            'language': doc['language'] if 'language' in doc else None,
            'data': image_data,
            'status': doc['status'],
            'activity': doc['activity'] if full_rights else [action
                                                             for action in doc['activity']
                                                             if action['user'] == user['_id']],
        },
        'relationships': {
            'source': {
                'data': {
                    'type': 'sources',
                    'id': doc['source_id'],
                }
            }
        }
    }


class JokeCollectionHandler(JSONAPICollectionHandler):
    """Handler for collection-level joke requests."""

    async def allow_get(self: 'JokeCollectionHandler', user: Union[Document, None]) -> None:
        """Allow all logged-in users to access the full list of jokes."""
        if user is not None:
            return
        raise JSONAPIError(403, [{'title': 'You are not authorised to access all jokes'}])

    async def create_get(self: 'JSONAPICollectionHandler', user: Union[Document, None]) -> Document:
        """Create a list of jokes."""
        async with couchdb() as session:
            jokes_db = await session['jokes']
            docs = []
            if 'admin' in user['groups'] or 'editor' in user['groups']:
                selector = {'_id': {'$gt': None}}
            else:
                selector = {'activity': {'$elemMatch': {'user': user['_id']}}}
            filter_ids = self.get_argument('filter[id]', default=None)
            if filter_ids is not None:
                if filter_ids.strip() == '':
                    return []
                else:
                    selector = {
                        '$and': [
                            selector,
                            {'$or': [{'_id': id_value} for id_value in filter_ids.split(',')]}
                        ]
                    }
            async for doc in jokes_db.find(selector=selector, sort=[{'status': 'asc'}]):
                docs.append(doc)
            return docs

    async def allow_post(self: 'JokeCollectionHandler', data: dict, user: Union[Document, None]) -> None:
        """Check whether the user is allowed to create a new joke.

        * All logged-in users are allowed to create new jokes.
        """
        if user is not None:
            return
        raise JSONAPIError(403, [{'title': 'You are not authorised to add joke data.'}])

    async def validate_post(self: 'JokeCollectionHandler', data: dict, user: Union[Document, None]) -> dict:
        """Validate the data for creating a new joke."""
        obj = validate({
            'type': type_schema('jokes'),
            'attributes': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'actions': {
                        'type': 'list',
                        'required': True,
                        'empty': False,
                        'minlength': 1,
                        'maxlength': 1,
                        'schema': {
                            'type': 'dict',
                            'schema': {
                                'coordinates': {
                                    'type': 'list',
                                    'required': True,
                                    'empty': False,
                                    'minlength': 4,
                                    'maxlength': 4,
                                    'schema': {
                                        'type': 'number',
                                    },
                                    'coerce': coerce_coordinates,
                                }
                            }
                        }
                    }
                }
            },
            'relationships': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'source': one_to_one_relationship_schema('sources')
                }
            }
        }, data, purge_unknown=True)
        source = None
        async with couchdb() as session:
            db = await session['sources']
            try:
                source = await db[obj['relationships']['source']['data']['id']]
            except aio_exc.NotFoundError:
                raise ValidationError({'relationships.source': 'This source does not exist'})
            source_attachment = Attachment(source, 'image')
            with Image.open(BytesIO(await source_attachment.fetch())) as img:
                obj['attributes']['data'] = img.crop(obj['attributes']['actions'][0]['coordinates'])
        return obj

    async def create_post(self: 'JokeCollectionHandler', data: dict, user: Union[Document, None]) -> Document:
        """Create a new joke."""
        async with couchdb() as session:
            uid = str(uuid1())
            db = await session['jokes']
            doc = await db.create(uid)
            doc['title'] = '[Untitled]'
            action = data['attributes']['actions'][0]
            doc['coordinates'] = action['coordinates']
            doc['categories'] = []
            doc['source_id'] = data['relationships']['source']['data']['id']
            doc['activity'] = [
                {
                    'action': 'extracted',
                    'user': user['_id'],
                    'timestamp': datetime.utcnow().timestamp(),
                    'params': action,
                }
            ]
            doc['status'] = 'extracted'
            if 'editor' in user['groups'] or 'admin' in user['groups']:
                doc['activity'].append({
                    'action': 'extraction-verified',
                    'user': user['_id'],
                    'timestamp': datetime.utcnow().timestamp(),
                })
                doc['status'] = 'extraction-verified'
            doc['transcriptions'] = {}
            await doc.save()
            image = Attachment(doc, 'image')
            buffer = BytesIO()
            data['attributes']['data'].save(buffer, format='png')
            await image.save(buffer.getvalue(), 'image/png')
            if doc['status'] == 'extraction-verified':
                async with mosquitto() as client:
                    await client.publish(f'jokes/{uid}/ocr')
            doc = await db[uid]
            return doc

    async def as_jsonapi(self: 'JokeCollectionHandler', doc: Document, user: Union[Document, None]) -> dict:
        """Return a single joke as JSONAPI."""
        return await as_jsonapi(doc, user)


class JokeItemHandler(JSONAPIItemHandler):
    """Handler for item-level joke requests."""

    async def allow_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether GET a joke is allowed.

        * Any logged-in user can access any joke.
        """
        if user is not None:
            return
        raise JSONAPIError(403, [{'title': 'You are not authorised to access this joke'}])

    async def create_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> Document:
        """Fetch a CouchDB document for the joke."""
        async with couchdb() as session:
            db = await session['jokes']
            try:
                doc = await db[iid]
                return doc
            except aio_exc.NotFoundError:
                raise JSONAPIError(404, [{'title': 'This joke does not exist'}])

    async def allow_put(self: 'JokeItemHandler', iid: str, data: dict, user: Union[Document, None]) -> None:
        """Allow all logged-in users to update a joke.

        Which fields they may update is configured in :func:`~toja.server.handlers.joke.validate_put`.
        """
        if user is not None:
            return
        raise JSONAPIError(403, [{'title': 'You are not authorised to update this joke'}])

    async def validate_put(self: 'JokeItemHandler', iid: str, data: dict, user: Union[Document, None]) -> dict:
        """Validate that the PUT data is valid."""
        async with couchdb() as session:
            db = await session['jokes']
            joke = await db[iid]
            relationships = {
                'source': one_to_one_relationship_schema('sources', value=joke['source_id'])
            }
            attributes = {}
            actions = []
            if 'admin' in user['groups'] or 'editor' in user['groups']:
                actions.append({
                    'coordinates': {
                        'type': 'list',
                        'required': False,
                        'empty': False,
                        'minlength': 4,
                        'maxlength': 4,
                        'schema': {
                            'type': 'number',
                        },
                        'coerce': coerce_coordinates,
                    }
                })
                actions.append({
                    'verified_transcription': {
                        'type': 'dict'
                    }
                })
                actions.append({
                    'annotated': {
                        'type': 'dict'
                    }
                })
                actions.append({
                    'categories': {
                        'type': 'list',
                        'schema': {
                            'type': 'string',
                            'empty': False,
                            'allowed': ['pun', 'dialogue', 'story', 'wit-wisdom', 'conundrum', 'verse',
                                        'definition', 'factoid'],
                        }
                    }
                })
                actions.append({
                    'topics': {
                        'type': 'string',
                    }
                })
                actions.append({
                    'language': {
                        'type': 'string',
                        'allowed': ['en'],
                    }
                })
                actions.append({
                    'status': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                        'allowed': ['extraction-verified', 'annotated', 'published']
                    }
                })
            else:
                if joke['status'] == 'extracted':
                    actions.append({
                        'coordinates': {
                            'type': 'list',
                            'required': False,
                            'empty': False,
                            'minlength': 4,
                            'maxlength': 4,
                            'schema': {
                                'type': 'number',
                            },
                            'coerce': coerce_coordinates,
                        }
                    })
                    user_performed_extraction = False
                    for activity in joke['activity']:
                        if activity['action'] == 'extracted' and activity['user'] == user['_id']:
                            user_performed_extraction = True
                    if not user_performed_extraction:
                        actions.append({
                            'status': {
                                'type': 'string',
                                'required': False,
                                'empty': False,
                                'allowed': ['extraction-verified']
                            }
                        })
                if joke['status'] == 'auto-transcribed':
                    user_performed_extraction = False
                    for activity in joke['activity']:
                        if activity['user'] == user['_id']:
                            if activity['action'] == 'extracted' or activity['action'] == 'extraction-verified':
                                user_performed_extraction = True
                    if not user_performed_extraction:
                        actions.append({
                            'transcription': {
                                'type': 'dict'
                            }
                        })
                if joke['status'] == 'auto-categorised':
                    actions.append({
                        'categories': {
                            'type': 'list',
                            'schema': {
                                'type': 'string',
                                'empty': False,
                                'allowed': ['pun', 'dialogue', 'story', 'wit-wisdom', 'conundrum', 'verse',
                                            'definition', 'factoid'],
                            }
                        }
                    })
                if joke['status'] == 'categories-verified':
                    user_performed_transcription = False
                    for activity in joke['activity']:
                        if activity['user'] == user['_id']:
                            if activity['action'] == 'transcribed' or activity['action'] == 'verified_transcription':
                                user_performed_transcription = True
                    if not user_performed_transcription:
                        actions.append({
                            'annotated': {
                                'type': 'dict'
                            }
                        })
            # Merge all the actions into the attributes
            attributes['actions'] = {
                'type': 'list',
                'schema': {
                    'anyof': [
                        {
                            'type': 'dict',
                            'required': True,
                            'empty': False,
                            'schema': action
                        }
                        for action in actions
                    ]
                },
                'default': []
            }
            schema = object_schema('jokes', iid, attributes, relationships)
            obj = validate(schema, data, purge_unknown=True)
            return obj

    async def create_put(self: 'JokeItemHandler', iid: str, data: dict, user: Union[Document, None]) -> Document:
        """Update a joke CouchDB document for a PUT request."""
        try:
            async with couchdb() as session:
                db = await session['jokes']
                doc = await db[iid]
                coords_changed = False
                for action in data['attributes']['actions']:
                    if 'coordinates' in action:
                        doc['coordinates'] = action['coordinates']
                        coords_changed = True
                        doc['activity'].append({
                            'action': 'extracted',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action,
                        })
                        doc['status'] = 'extracted'
                        if 'editor' in user['groups'] or 'admin' in user['groups']:
                            doc['activity'].append({
                                'action': 'extraction-verified',
                                'user': user['_id'],
                                'timestamp': datetime.utcnow().timestamp(),
                            })
                            doc['status'] = 'extraction-verified'
                        if 'auto' in doc['transcriptions']:
                            del doc['transcriptions']['auto']
                    elif 'transcription' in action:
                        doc['transcriptions'][user['_id']] = action['transcription']
                        doc['activity'].append({
                            'action': 'transcribe',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action,
                        })
                    elif 'verified_transcription' in action:
                        doc['transcriptions']['verified'] = action['verified_transcription']
                        doc['activity'].append({
                            'action': 'verified_transcription',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action,
                        })
                        doc['status'] = 'transcription-verified'
                    elif 'categories' in action:
                        doc['categories'] = action['categories']
                        doc['activity'].append({
                            'action': 'categories-verified',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action,
                        })
                        doc['status'] = 'categories-verified'
                    elif 'annotated' in action:
                        doc['transcriptions'][user['_id']] = action['annotated']
                        doc['activity'].append({
                            'action': 'annotated',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action
                        })
                    elif 'topics' in action:
                        doc['topics'] = action['topics']
                        doc['activity'].append({
                            'action': 'set-topics',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action
                        })
                    elif 'language' in action:
                        doc['language'] = action['language']
                        doc['activity'].append({
                            'action': 'set-language',
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                            'params': action
                        })
                    elif 'status' in action:
                        doc['status'] = action['status']
                        doc['activity'].append({
                                'action': action['status'],
                                'user': user['_id'],
                                'timestamp': datetime.utcnow().timestamp(),
                        })
                        if doc['status'] == 'annotated':
                            if user['_id'] in doc['transcriptions']:
                                doc['transcriptions']['annotated'] = doc['transcriptions'][user['_id']]
                        if doc['status'] == 'published':
                            if 'annotated' in doc['transcriptions']:
                                doc['transcriptions']['final'] = doc['transcriptions']['annotated']
                    else:
                        logger.debug(action)
                doc['updated'] = datetime.utcnow().timestamp()
                await doc.save()
                if coords_changed:
                    sources_db = await session['sources']
                    try:
                        source = await sources_db[data['relationships']['source']['data']['id']]
                    except aio_exc.NotFoundError:
                        raise ValidationError({'relationships.source': 'This source does not exist'})
                    source_attachment = Attachment(source, 'image')
                    buffer = BytesIO()
                    with Image.open(BytesIO(await source_attachment.fetch())) as img:
                        cropped = img.crop(action['coordinates'])
                        cropped.save(buffer, format='png')
                    image = Attachment(doc, 'image')
                    await image.save(buffer.getvalue(), 'image/png')
                    async with mosquitto() as client:
                        await client.publish(f'jokes/{iid}/ocr')
                if doc['status'] == 'transcription-verified':
                    async with mosquitto() as client:
                        await client.publish(f'jokes/{iid}/categorise')
                if doc['status'] == 'published':
                    async with mosquitto() as client:
                        await client.publish(f'jokes/{iid}/publish')
                doc = await db[iid]
                return doc
        except aio_exc.NotFoundError:
            raise JSONAPIError(404, [{'title': 'This joke does not exist'}])

    async def allow_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether DELETE requests are allowed.

        * Admins and editors are allowed to delete a joke at any stage.
        * The user who extracted the joke can delete it as long as it has not been confirmed.
        """
        if user is not None:
            if 'admin' in user['groups'] or 'editor' in user['groups']:
                return
            else:
                async with couchdb() as session:
                    db = await session['jokes']
                    joke = await db[iid]
                    if joke['status'] == 'extracted':
                        for activity in joke['activity']:
                            if activity['action'] == 'extracted' and activity['user'] == user['_id']:
                                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to delete this joke'}])

    async def create_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Delete the CouchDB document for the joke."""
        try:
            async with couchdb() as session:
                db = await session['jokes']
                doc = await db[iid]
                await doc.delete()
        except aio_exc.NotFoundError:
            raise JSONAPIError(404, [{'title': 'This joke does not exist'}])

    async def as_jsonapi(self: 'JokeItemHandler', doc: Document, user: Union[Document, None]) -> dict:
        """Return a single joke as JSONAPI."""
        return await as_jsonapi(doc, user)
