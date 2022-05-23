"""Source-related request handlers."""
from aiocouch import Document, exception as aio_exc
from aiocouch.attachment import Attachment
from base64 import b64decode, b64encode
from datetime import datetime
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from typing import Union
from uuid import uuid1

from .base import JSONAPICollectionHandler, JSONAPIItemHandler, JSONAPIError
from toja.utils import async_gen_to_list, couchdb
from toja.validation import validate, ValidationError


async def as_jsonapi(doc: Document, user: Union[Document, None]) -> dict:
    """Return a single source as JSONAPI."""
    async with couchdb() as session:
        db = await session['sources']
        doc = await db[doc['_id']]
        image = Attachment(doc, 'image')
        image_data = f'data:image/png;base64,{b64encode(await image.fetch()).decode("utf-8")}'
        db = await session['jokes']
        jokes = await async_gen_to_list(db.find({'source_id': doc['_id']}))
        jokes.sort(key=lambda j: j['coordinates'][1])
        joke_ids = list(map(lambda joke: {'type': 'jokes', 'id': joke['_id']}, jokes))
    return {
        'id': doc['_id'],
        'type': 'sources',
        'attributes': {
            'type': doc['type'],
            'title': doc['title'],
            'subtitle': doc['subtitle'],
            'date': doc['date'],
            'location': doc['location'],
            'publisher': doc['publisher'],
            'page_numbers': doc['page_numbers'],
            'data': image_data,
            'created': doc['created'],
        },
        'relationships': {
            'creator': {
                'data': {
                    'type': 'users',
                    'id': doc['creator'],
                },
            },
            'jokes': {
                'data': joke_ids,
            },
        },
    }


class SourceCollectionHandler(JSONAPICollectionHandler):
    """Handler for collection-level source requests."""

    async def allow_get(self: 'SourceCollectionHandler', user: Union[Document, None]) -> None:
        """Allow users with the admin and provider roles to access the full list of sources."""
        if user is not None:
            if 'admin' in user['groups'] or 'provider' in user['groups']:
                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to access all sources'}])

    async def create_get(self: 'JSONAPICollectionHandler', user: Union[Document, None]) -> Document:
        """Create a list of sources."""
        async with couchdb() as session:
            sources_db = await session['sources']
            docs = []
            if 'admin' in user['groups']:
                selector = {'title': {'$exists': True}}
            else:
                selector = {'creator': user['_id']}
            async for doc in sources_db.find(selector=selector, sort=[{'created': 'asc'}]):
                docs.append(doc)
            return docs

    async def allow_post(self: 'SourceCollectionHandler', data: dict, user: Union[Document, None]) -> None:
        """Allow POST requests for admins and providers."""
        if user is not None:
            if 'admin' in user['groups'] or 'provider' in user['groups']:
                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to add source data.'}])

    async def validate_post(self: 'SourceCollectionHandler', data: dict, user: Union[Document, None]) -> dict:
        """Validate the data for creating a new source."""
        obj = validate({
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['sources']
            },
            'attributes': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'type': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                        'allowed': ['newspaper', 'book']
                    },
                    'title': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    },
                    'subtitle': {
                        'type': 'string',
                        'required': True,
                    },
                    'date': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    },
                    'location': {
                        'type': 'string',
                        'required': True,
                    },
                    'publisher': {
                        'type': 'string',
                        'required': True,
                    },
                    'page_numbers': {
                        'type': 'string',
                        'required': True,
                    },
                    'data': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                        'regex': r'data:image/(png|jpeg);base64,[a-zA-Z0-9+/=]+'
                    }
                }
            }
        }, data, purge_unknown=True)
        image_data = data['attributes']['data'][data['attributes']['data'].find(',') + 1:]
        format = data['attributes']['data'][data['attributes']['data'].find('/') + 1:data['attributes']['data'].find(';')]  # noqa: E501
        try:
            with Image.open(BytesIO(b64decode(image_data)), formats=[format]) as img:
                img.load()
                obj['attributes']['data'] = img
        except UnidentifiedImageError:
            raise ValidationError({'attributes.data': 'This is not a supported image format'})
        return obj

    async def create_post(self: 'SourceCollectionHandler', data: dict, user: Union[Document, None]) -> Document:
        """Create a new source."""
        async with couchdb() as session:
            uid = str(uuid1())
            db = await session['sources']
            doc = await db.create(uid)
            doc['type'] = data['attributes']['type']
            doc['title'] = data['attributes']['title']
            doc['subtitle'] = data['attributes']['subtitle']
            doc['date'] = data['attributes']['date']
            doc['location'] = data['attributes']['location']
            doc['publisher'] = data['attributes']['publisher']
            doc['page_numbers'] = data['attributes']['page_numbers']
            doc['creator'] = user['_id']
            doc['created'] = datetime.utcnow().timestamp()
            await doc.save()
            image = Attachment(doc, 'image')
            buffer = BytesIO()
            data['attributes']['data'].save(buffer, format='png')
            await image.save(buffer.getvalue(), 'image/png')
            doc = await db[uid]
            return doc

    async def as_jsonapi(self: 'SourceCollectionHandler', doc: Document, user: Union[Document, None]) -> dict:
        """Return a single source as JSONAPI."""
        return await as_jsonapi(doc, user)


class SourceItemHandler(JSONAPIItemHandler):
    """Handler for item-level source requests."""

    async def allow_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether GET a source is allowed."""
        if user is not None:
            return
        raise JSONAPIError(403, [{'title': 'You are not authorised to access this source'}])

    async def create_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> Document:
        """Fetch a CouchDB document for the source."""
        async with couchdb() as session:
            db = await session['sources']
            try:
                doc = await db[iid]
                return doc
            except aio_exc.NotFoundError:
                raise JSONAPIError(404, [{'title': 'This source does not exist'}])

    async def allow_put(self: 'SourceItemHandler', iid: str, data: dict, user: Union[Document, None]) -> None:
        """Check whether PUT requests are allowed."""
        if user is not None:
            if 'admin' in user['groups']:
                return
            elif 'provider' in user['groups']:
                async with couchdb() as session:
                    db = await session['sources']
                    async for source in db.find({'_id': iid, 'creator': user['_id']}):
                        return
        raise JSONAPIError(403, [{'title': 'You are not authorised to update this source'}])

    async def validate_put(self: 'SourceItemHandler', iid: str, data: dict, user: Union[Document, None]) -> dict:
        """Validate that the PUT data is valid."""
        schema = {
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['sources']
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
                    'title': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                    },
                    'subtitle': {
                        'type': 'string',
                        'required': False,
                    },
                    'date': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                    },
                    'location': {
                        'type': 'string',
                        'required': False,
                    },
                    'publisher': {
                        'type': 'string',
                        'required': False,
                    },
                    'page_numbers': {
                        'type': 'string',
                        'required': False,
                    },
                    'data': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                        'regex': r'data:image/(png|jpeg);base64,[a-zA-Z0-9+/=]+'
                    }
                }
            }
        }
        obj = validate(schema, data, purge_unknown=True)
        if 'data' in data['attributes']:
            image_data = data['attributes']['data'][data['attributes']['data'].find(',') + 1:]
            format = data['attributes']['data'][data['attributes']['data'].find('/') + 1:data['attributes']['data'].find(';')]  # noqa: E501
            try:
                with Image.open(BytesIO(b64decode(image_data)), formats=[format]) as img:
                    img.load()
                    obj['attributes']['data'] = img
            except UnidentifiedImageError:
                raise ValidationError({'attributes.data': 'This is not a supported image format'})
        return obj

    async def create_put(self: 'SourceItemHandler', iid: str, data: dict, user: Union[Document, None]) -> Document:
        """Update a source CouchDB document for a PUT request."""
        try:
            async with couchdb() as session:
                db = await session['sources']
                doc = await db[iid]
                if 'type' in data['attributes']:
                    doc['type'] = data['attributes']['type']
                if 'title' in data['attributes']:
                    doc['title'] = data['attributes']['title']
                if 'subtitle' in data['attributes']:
                    doc['subtitle'] = data['attributes']['subtitle']
                if 'date' in data['attributes']:
                    doc['date'] = data['attributes']['date']
                if 'publisher' in data['attributes']:
                    doc['publisher'] = data['attributes']['publisher']
                if 'location' in data['attributes']:
                    doc['location'] = data['attributes']['location']
                if 'page_numbers' in data['attributes']:
                    doc['page_numbers'] = data['attributes']['page_numbers']
                if 'data' in data['attributes']:
                    pass
                doc['updated'] = datetime.utcnow().timestamp()
                await doc.save()
                if 'data' in data['attributes']:
                    image = Attachment(doc, 'image')
                    buffer = BytesIO()
                    data['attributes']['data'].save(buffer, format='png')
                    await image.save(buffer.getvalue(), 'image/png')
                doc = await db[iid]
                return doc
        except aio_exc.NotFoundError:
            raise JSONAPIError(404, [{'title': 'This source does not exist'}])

    async def allow_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether DELETE requests are allowed."""
        if user is not None:
            if 'admin' in user['groups']:
                return
            elif 'provider' in user['groups']:
                async with couchdb() as session:
                    db = await session['sources']
                    async for source in db.find({'_id': iid, 'creator': user['_id']}):
                        return
        raise JSONAPIError(403, [{'title': 'You are not authorised to delete this source'}])

    async def create_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Delete the CouchDB document for the source."""
        try:
            async with couchdb() as session:
                db = await session['sources']
                doc = await db[iid]
                await doc.delete()
        except aio_exc.NotFoundError:
            raise JSONAPIError(404, [{'title': 'This source does not exist'}])

    async def as_jsonapi(self: 'SourceItemHandler', doc: Document, user: Union[Document, None]) -> dict:
        """Return a single source as JSONAPI."""
        return await as_jsonapi(doc, user)
