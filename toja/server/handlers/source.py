"""Source-related request handlers."""
from aiocouch import Document
from aiocouch.attachment import Attachment
from base64 import b64decode, b64encode
from datetime import datetime
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from typing import Union
from uuid import uuid1

from .base import JSONAPICollectionHandler, JSONAPIError
from toja.utils import couchdb
from toja.validation import validate, ValidationError


class SourceCollectionHandler(JSONAPICollectionHandler):
    """Handler for collection-level source requests."""

    async def allow_get(self: 'SourceCollectionHandler', user: Union[Document, None]) -> None:
        """Allow users with the admin and provider roles to access the full list of sources."""
        if user is not None:
            if 'admin' in user['groups'] or 'provider' in user['groups']:
                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to access all sources'}])

    async def create_get(self: 'JSONAPICollectionHandler', user: Union[Document, None]) -> Document:
        """Create a new CouchDB document."""
        async with couchdb() as session:
            users_db = await session['users']
            docs = []
            async for doc in users_db.find(selector={'name': {'$exists': True}}, sort=[{'email': 'asc'}]):
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
            doc['created'] = datetime.utcnow().timestamp()
            await doc.save()
            image = Attachment(doc, 'image')
            buffer = BytesIO()
            data['attributes']['data'].save(buffer, format='png')
            await image.save(buffer.getvalue(), 'image/png')
            doc = await db[uid]
            return doc

    async def as_jsonapi(self: 'SourceCollectionHandler', doc: Document) -> dict:
        """Return a single source as JSONAPI."""
        async with couchdb() as session:
            db = await session['sources']
            doc = await db[doc['_id']]
            image = Attachment(doc, 'image')
            image_data = f'data:image/png;base64,{b64encode(await image.fetch()).decode("utf-8")}'
        return {
            'id': doc['_id'],
            'type': 'users',
            'attributes': {
                'type': doc['type'],
                'title': doc['title'],
                'subtitle': doc['subtitle'],
                'date': doc['date'],
                'location': doc['location'],
                'publisher': doc['publisher'],
                'page_numbers': doc['page_numbers'],
                'data': f'data:image/png;base64,{image_data}',
                'created': doc['created'],
            }
        }
