"""User-related request handlers."""
from aiocouch import Document

from secrets import token_hex
from typing import Union
from urllib.parse import urlencode

from toja.utils import couchdb, send_email, config
from toja.validation import validate, ValidationError
from uuid import uuid1
from .base import JSONAPICollectionHandler


class UserCollectionHandler(JSONAPICollectionHandler):
    """Handler for collection-level user requests."""

    async def allow_post(self: 'UserCollectionHandler', data: dict, user: Union[Document, None]) -> None:
        """Allow all POST requests."""
        pass

    async def validate_post(self: 'UserCollectionHandler', data: dict, user: Union[Document, None]) -> dict:
        """Validate the data for creating a new user."""
        obj = validate({
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['users']
            },
            'attributes': {
                'type': 'dict',
                'schema': {
                    'email': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                        'check_with': 'validate_email',
                        'coerce': 'email',
                    },
                    'name': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    }
                }
            }
        }, data)
        async with couchdb() as session:
            db = await session['users']
            async for user in db.find({'email': obj['attributes']['email']}):
                raise ValidationError({'attributes.email': 'This e-mail address is already registered'})
        return obj

    async def create_post(self: 'UserCollectionHandler', data: dict, user: Union[Document, None]) -> None:
        """Create a new user."""
        async with couchdb() as session:
            uid = str(uuid1())
            db = await session['users']
            async with Document(db, uid) as doc:
                doc['name'] = data['attributes']['name']
                doc['email'] = data['attributes']['email']
                if (await db.info())['doc_count'] == 0:
                    doc['groups'] = ['admin']
                else:
                    doc['groups'] = []
                doc['token'] = token_hex(128)
            doc = await db[uid]
            send_email(doc['email'], 'Log in to The Old Joke Archive', f'''Hello {doc["name"]},

Please use the following link to log into The Old Joke Archive:

{config()['server']['base']}/app/user/log-in?{urlencode((('email', doc["email"]), ('token', doc["token"]), ('remember', False)))}

The Old Joke Automaton.
''')  # noqa: E501
            return doc

    async def as_jsonapi(self: 'UserCollectionHandler', doc: Document) -> dict:
        """Return a single user as JSONAPI."""
        return {
            'id': doc['_id'],
            'type': 'users',
            'attributes': {
                'name': doc['name'],
                'email': doc['email'],
                'groups': doc['groups'],
            }
        }
