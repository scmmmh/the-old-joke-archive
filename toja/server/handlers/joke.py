"""Joke-related request handlers.

The joke status workflow is as follows:

* Extracted
* Extraction-verified
* Auto-transcribed
* Transcribed
* Transcription-verified
* Category-verified
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
from toja.validation import validate, ValidationError, type_schema, one_to_one_relationship_schema


def coerce_coordinates(value: list) -> list:
    """Coerce the coordinates into an integer bounding box."""
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
        """Allow POST requests for admins and providers."""
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
                'transcribed': [],
                'transcription-verified': None,
                'category-verified': None,
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
        """Check whether GET a joke is allowed."""
        if user is not None:
            if 'admin' in user['groups'] or 'editor' in user['groups']:
                return
        async with couchdb() as session:
            db = await session['jokes']
            try:
                doc = await db[iid]
                if doc['status'] == 'published':
                    return
            except aio_exc.NotFoundError:
                pass
            if user is not None:
                for activity in ['extracted', 'extraction-verified', 'transcription-verified', 'category-verified',
                                 'annotated', 'annotation-verified']:
                    if doc['activity'][activity] and doc['activity'][activity]['user'] == user['_id']:
                        return
                for transcriber in doc['activity']['transcribed']:
                    if transcriber['user'] == user[':id']:
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
        """Check whether PUT requests are allowed."""
        if user is not None:
            if 'admin' in user['groups']:
                return
            elif 'provider' in user['groups']:
                async with couchdb() as session:
                    db = await session['jokes']
                    async for joke in db.find({'_id': iid, 'creator': user['_id']}):
                        return
        raise JSONAPIError(403, [{'title': 'You are not authorised to update this joke'}])

    async def validate_put(self: 'JokeItemHandler', iid: str, data: dict, user: Union[Document, None]) -> dict:
        """Validate that the PUT data is valid."""
        async with couchdb() as session:
            db = await session['jokes']
            doc = await db[iid]
            source_id = doc['source_id']
        schema = {
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['jokes']
            },
            'id': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': [iid]
            },
            'attributes': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'type': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                        'allowed': ['newspaper', 'book']
                    },
                    'data': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                        'regex': r'data:image/(png|jpeg);base64,[a-zA-Z0-9+/=]+'
                    }
                }
            },
            'relationships': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'source': one_to_one_relationship_schema('sources', value=source_id)
                }
            }
        }
        async with couchdb() as session:
            db = await session['jokes']
            doc = await db[iid]
            if doc['status'] in ['extracted', 'extraction-verified'] or \
                    'admin' in user['groups'] or 'editor' in user['groups']:
                schema['attributes']['schema']['coordinates'] = {
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
            if doc['status'] == 'auto-transcribed' or 'admin' in user['groups'] or 'editor' in user['groups']:
                schema['attributes']['schema']['transcriptions'] = {
                    'type': 'dict',
                    'required': False,
                    'empty': False,
                    'schema': {
                        user['_id']: {
                            'type': 'dict'
                        }
                    }
                }
        obj = validate(schema, data, purge_unknown=True)
        if 'coordinates' in obj['attributes']:
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

    async def create_put(self: 'JokeItemHandler', iid: str, data: dict, user: Union[Document, None]) -> Document:
        """Update a joke CouchDB document for a PUT request."""
        try:
            async with couchdb() as session:
                db = await session['jokes']
                doc = await db[iid]
                coords_changed = False
                if 'type' in data['attributes']:
                    doc['type'] = data['attributes']['type']
                if 'coordinates' in data['attributes'] and doc['coordinates'] != data['attributes']['coordinates']:
                    doc['coordinates'] = data['attributes']['coordinates']
                    coords_changed = True
                if coords_changed and 'transcriptions' in doc and 'auto' in doc['transcriptions']:
                    del doc['transcriptions']['auto']
                if 'transcriptions' in data['attributes'] and user['_id'] in data['attributes']['transcriptions']:
                    doc['transcriptions'][user['_id']] = data['attributes']['transcriptions'][user['_id']]
                if 'admin' in user['groups'] or 'editor' in user['groups']:
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
                        doc['status'] = 'transcription-verified'
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
        """Check whether DELETE requests are allowed."""
        if user is not None:
            if 'admin' in user['groups']:
                return
            elif 'provider' in user['groups']:
                async with couchdb() as session:
                    db = await session['jokes']
                    async for joke in db.find({'_id': iid, 'creator': user['_id']}):
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
