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
    return {
        'id': doc['_id'],
        'type': 'jokes',
        'attributes': {
            'title': doc['title'],
            'coordinates': doc['coordinates'],
            'transcriptions': dict([(key, value)
                                    for key, value in doc['transcriptions'].items()
                                    if key in ['auto', 'final', user['_id'] if user else None]]),
            'data': image_data,
            'status': doc['status'],
            'activity': doc['activity'],
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
                selector = {'title': {'$exists': True}}
            else:
                selector = {'$or': [
                    {'activity.extracted.user': user['_id']},
                    {'activity.extraction-verified.user': user['_id']},
                    {'activity.transcribed.user': user['_id']},
                    {'activity.transcription-verified.user': user['_id']},
                    {'activity.category-verified.user': user['_id']},
                    {'activity.annotated.user': user['_id']},
                    {'activity.annotation-verified.user': user['_id']},
                ]}
            filter_ids = self.get_argument('filter[id]', default=None)
            if filter_ids:
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
                obj['attributes']['data'] = img.crop(obj['attributes']['coordinates'])
        return obj

    async def create_post(self: 'JokeCollectionHandler', data: dict, user: Union[Document, None]) -> Document:
        """Create a new joke."""
        async with couchdb() as session:
            uid = str(uuid1())
            db = await session['jokes']
            doc = await db.create(uid)
            doc['title'] = '[Untitled]'
            doc['coordinates'] = data['attributes']['coordinates']
            doc['source_id'] = data['relationships']['source']['data']['id']
            doc['activity'] = {
                'extracted': {
                    'user': user['_id'],
                    'timestamp': datetime.utcnow().timestamp(),
                },
                'extraction-verified': None,
                'transcribed': {},
                'transcription-verified': None,
                'categories-verified': None,
                'annotated': None,
                'annotation-verified': None,
            }
            if 'editor' in user['groups'] or 'admin' in user['groups']:
                doc['activity']['extracted'] = {
                    'user': user['_id'],
                    'timestamp': datetime.utcnow().timestamp(),
                }
                doc['activity']['extraction-verified'] = {
                    'user': user['_id'],
                    'timestamp': datetime.utcnow().timestamp(),
                }
                doc['status'] = 'extraction-verified'
            else:
                doc['activity']['extracted'] = {
                    'user': user['_id'],
                    'timestamp': datetime.utcnow().timestamp(),
                }
                doc['status'] = 'extracted'
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
        allow_everything = 'admin' in user['groups'] or 'editor' in user['groups']
        async with couchdb() as session:
            db = await session['jokes']
            joke = await db[iid]
            relationships = {
                'source': one_to_one_relationship_schema('sources', value=joke['source_id'])
            }
            attributes = {}
            if joke['status'] == 'extracted' or allow_everything:
                # Validation for coordinate changes
                attributes['coordinates'] = {
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
            if (joke['status'] == 'extracted' and user['_id'] != joke['activity']['extracted']['user']) \
                    or allow_everything:
                # Allow verifying the extraction unless the current user is the user who extracted the joke
                attributes['status'] = {
                    'type': 'string',
                    'required': False,
                    'empty': False,
                    'allowed': ['extraction-verified']
                }
            if joke['status'] == 'transcribed' or joke['status'] == 'auto-transcribed' or allow_everything:
                attributes['transcriptions'] = {
                    'type': 'dict',
                    'required': False,
                    'schema': {
                        user['_id']: {
                            'type': 'dict',
                        }
                    }
                }
            if joke['status'] == 'auto-categorised' or allow_everything:
                attributes['categories'] = {
                    'type': 'list',
                    'required': False,
                    'schema': {
                        'type': 'string'
                    }
                }
                attributes['status'] = {
                    'type': 'string',
                    'required': False,
                    'empty': False,
                    'allowed': ['categories-verified'] if not allow_everything else ['extraction-verified',
                                                                                     'categories-verified']
                }
            if joke['status'] == 'categories-verified' or allow_everything:
                attributes['transcriptions'] = {
                    'type': 'dict',
                    'required': False,
                    'schema': {
                        user['_id']: {
                            'type': 'dict',
                        }
                    }
                }
                attributes['status'] = {
                    'type': 'string',
                    'required': False,
                    'empty': False,
                    'allowed': ['annotated'] if not allow_everything else ['extraction-verified',
                                                                           'categories-verified',
                                                                           'annotated']
                }
            if joke['status'] == 'annotated' and allow_everything:
                attributes['status'] = {
                    'type': 'string',
                    'required': False,
                    'empty': False,
                    'allowed': ['annotations-verified'] if not allow_everything else ['extraction-verified',
                                                                                      'categories-verified',
                                                                                      'annotated',
                                                                                      'annotations-verified']
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
                if 'coordinates' in data['attributes'] and doc['coordinates'] != data['attributes']['coordinates']:
                    # Update the joke's coordinates
                    doc['coordinates'] = data['attributes']['coordinates']
                    coords_changed = True
                    if 'transcriptions' in doc and 'auto' in doc['transcriptions']:
                        del doc['transcriptions']['auto']
                    doc['activity']['extracted'] = {
                        'user': user['_id'],
                        'timtestamp': datetime.utcnow().timestamp(),
                    }
                    if 'editor' in user['groups'] or 'admin' in user['groups']:
                        doc['activity']['extraction-verified'] = {
                            'user': user['_id'],
                            'timtestamp': datetime.utcnow().timestamp(),
                        }
                        doc['status'] = 'extraction-verified'
                    else:
                        doc['status'] = 'extracted'
                if 'transcriptions' in data['attributes'] and user['_id'] in data['attributes']['transcriptions']:
                    doc['transcriptions'][user['_id']] = data['attributes']['transcriptions'][user['_id']]
                    doc['activity']['transcribed'][user['_id']] = datetime.utcnow().timestamp()
                    if 'editor' in user['groups'] or 'admin' in user['groups']:
                        doc['transcriptions']['final'] = data['attributes']['transcriptions'][user['_id']]
                        doc['activity']['transcription-verified'] = {
                            'user': user['_id'],
                            'timtestamp': datetime.utcnow().timestamp(),
                        }
                        doc['status'] = 'transcription-verified'
                if 'status' in data['attributes']:
                    doc['status'] = data['attributes']['status']
                    if data['attributes']['status'] != 'transcribed':
                        doc['activity'][data['attributes']['status']] = {
                            'user': user['_id'],
                            'timtestamp': datetime.utcnow().timestamp(),
                        }

                """if 'admin' in user['groups'] or 'editor' in user['groups']:
                    # Changes to save if the user is an editor or admin
                    if 'transcriptions' in data['attributes'] and user['_id'] in data['attributes']['transcriptions']:
                        doc['transcriptions']['final'] = data['attributes']['transcriptions'][user['_id']]
                        found = False
                        for activity in doc['activity']['transcribed']:
                            if activity['user'] == user['_id']:
                                found = True
                                activity['timestamp'] = datetime.utcnow().timestamp()
                                break
                        if not found:
                            doc['activity']['transcribed'].append({
                                'user': user['_id'],
                                'timestamp': datetime.utcnow().timestamp(),
                            })
                        doc['activity']['transcription-verified'] = {
                            'user': user['_id'],
                            'timestamp': datetime.utcnow().timestamp(),
                        }
                        doc['status'] = 'transcription-verified'"""
                doc['updated'] = datetime.utcnow().timestamp()
                await doc.save()
                if coords_changed and 'data' in data['attributes']:
                    image = Attachment(doc, 'image')
                    buffer = BytesIO()
                    data['attributes']['data'].save(buffer, format='png')
                    await image.save(buffer.getvalue(), 'image/png')
                    async with mosquitto() as client:
                        await client.publish(f'jokes/{iid}/ocr')
                if doc['status'] == 'transcription-verified':
                    async with mosquitto() as client:
                        await client.publish(f'jokes/{iid}/categorise')
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
                    if joke['status'] == 'extracted' and joke['activity']['extracted']['user'] == user['_id']:
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
