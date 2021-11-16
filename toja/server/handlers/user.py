"""User-related request handlers."""
import bcrypt
import logging

from aiocouch import Document, exception as aio_exc

from secrets import token_hex
from typing import Union
from urllib.parse import urlencode

from toja.utils import couchdb, send_email, config, JSONAPIError
from toja.validation import validate, ValidationError
from uuid import uuid1
from .base import JSONAPIHandler, JSONAPICollectionHandler, JSONAPIItemHandler


logger = logging.getLogger(__name__)


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
                'required': True,
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

    async def create_post(self: 'UserCollectionHandler', data: dict, user: Union[Document, None]) -> Document:
        """Create a new user."""
        async with couchdb() as session:
            uid = str(uuid1())
            db = await session['users']
            doc = await db.create(uid)
            doc['name'] = data['attributes']['name']
            doc['email'] = data['attributes']['email']
            doc['status'] = 'new'
            if (await db.info())['doc_count'] == 0:
                doc['groups'] = ['admin']
            else:
                doc['groups'] = []
            doc['token'] = token_hex(128)
            await doc.save()
            doc = await db[uid]
            send_email(doc['email'], 'Sign up to The Old Joke Archive', f'''Hello {doc["name"]},

Please use the following link to confirm signing up to The Old Joke Archive:

{config()['server']['base']}/app/user/confirm?{urlencode((('id', doc["_id"]), ('token', doc["token"])))}

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


class UserItemHandler(JSONAPIItemHandler):
    """Handler for item-level collection requests."""

    async def allow_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether GET requests are allowed."""
        if user is not None:
            if 'admin' in user['groups'] or 'admin:users' in user['groups'] or user['_id'] == iid:
                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to access this user'}])

    async def create_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> Document:
        """Fetch a CouchDB document for the user."""
        async with couchdb() as session:
            db = await session['users']
            try:
                doc = await db[iid]
                return doc
            except aio_exc.NotFoundError:
                raise JSONAPIError(404, [{'title': 'This user does not exist'}])

    async def allow_put(self: 'UserItemHandler', iid: str, data: dict, user: Union[Document, None]) -> None:
        """Check whether PUT requests are allowed."""
        if user is not None:
            if 'admin' in user['groups'] or 'admin:users' in user['groups'] or user['_id'] == iid:
                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to update this user'}])

    async def validate_put(self: 'UserItemHandler', iid: str, data: dict, user: Union[Document, None]) -> dict:
        """Validate that the PUT data is valid."""
        schema = {
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['users']
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
                    'email': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                        'check_with': 'validate_email',
                        'coerce': 'email',
                    },
                    'name': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                    },
                    'password': {
                        'type': 'string',
                        'empty': False,
                    }
                }
            }
        }
        if user and ('admin' in user['groups'] or 'admin:user' in user['groups']):
            schema['attributes']['schema']['groups'] = {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            }
        obj = validate(schema, data)
        if 'email' in obj['attributes']:
            async with couchdb() as session:
                db = await session['users']
                async for user in db.find({'email': obj['attributes']['email']}):
                    if user['_id'] != iid:
                        raise ValidationError({'attributes.email': 'This e-mail address is already registered'})
        return obj

    async def create_put(self: 'UserItemHandler', iid: str, data: dict, user: Union[Document, None]) -> Document:
        """Update a user CouchDB document for a PUT request."""
        try:
            async with couchdb() as session:
                db = await session['users']
                doc = await db[iid]
                if 'email' in data['attributes']:
                    doc['email'] = data['attributes']['email']
                if 'name' in data['attributes']:
                    doc['name'] = data['attributes']['name']
                if 'groups' in data['attributes']:
                    doc['groups'] = data['attributes']['groups']
                if 'password' in data['attributes']:
                    doc['password'] = bcrypt.hashpw(data['attributes']['password'].encode('utf-8'),
                                                    bcrypt.gensalt()).decode()
                if doc['status'] == 'new':
                    doc['status'] = 'active'
                await doc.save()
                doc = await db[iid]
                return doc
        except aio_exc.NotFoundError:
            raise JSONAPIError(404, [{'title': 'This user does not exist'}])

    async def as_jsonapi(self: 'UserItemHandler', doc: Document) -> dict:
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

    async def allow_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether DELETE requests are allowed."""
        if user is not None:
            if 'admin' in user['groups'] or 'admin:users' in user['groups'] or user['_id'] == iid:
                return
        raise JSONAPIError(403, [{'title': 'You are not authorised to delete this user'}])

    async def create_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Delete the CouchDB document for the user."""
        try:
            async with couchdb() as session:
                db = await session['users']
                doc = await db[iid]
                await doc.delete()
        except aio_exc.NotFoundError:
            raise JSONAPIError(404, [{'title': 'This user does not exist'}])


class LoginHandler(JSONAPIHandler):
    """Handler for logging the user in."""

    def validate_post(self: 'LoginHandler', data: dict) -> dict:
        """Validate that the posted ``data`` is valid."""
        schema = {
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['users']
            },
            'attributes': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'email': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                        'check_with': 'validate_email',
                        'coerce': 'email',
                    },
                    'password': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    },
                }
            }
        }
        return validate(schema, data)

    async def post(self: 'LoginHandler') -> None:
        """Handle a login request."""
        try:
            async with couchdb() as session:
                db = await session['users']
                user = self.validate_post(await self.jsonapi_body())
                db_obj = None
                async for tmp in db.find({'email': user['attributes']['email'],
                                          'status': 'active'}):
                    if 'password' in tmp and bcrypt.checkpw(user['attributes']['password'].encode('utf-8'),
                                                            tmp['password'].encode('utf-8')):
                        db_obj = tmp
                if db_obj is None:
                    raise JSONAPIError(403, [{'title': 'This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.',  # noqa: 501
                                              'password': 'This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.'}])  # noqa: 501
                db_obj['token'] = token_hex(128)
                await db_obj.save()
                self.set_status(200)
                self.write({
                    'data': {
                        'type': 'users',
                        'id': db_obj['_id'],
                        'attributes': {
                            'token': db_obj['token']
                        }
                    }
                })
        except aio_exc.NotFoundError:
            raise JSONAPIError(403, [{'title': 'This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.',  # noqa: 501
                                      'password': 'This e-mail address is not registered, the password is incorrect, or the account is locked due to inactivity.'}])  # noqa: 501

    def validate_put(self: 'LoginHandler', data: dict) -> dict:
        """Validate that the putted ``data`` is valid."""
        schema = {
            'type': {
                'type': 'string',
                'required': True,
                'empty': False,
                'allowed': ['users']
            },
            'id': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'attributes': {
                'type': 'dict',
                'required': True,
                'schema': {
                    'token': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    },
                }
            }
        }
        return validate(schema, data)

    async def put(self: 'LoginHandler') -> None:
        """Confirm the user."""
        try:
            async with couchdb() as session:
                db = await session['users']
                user = self.validate_put(await self.jsonapi_body())
                db_obj = db[user['id']]
                if db_obj['status'] != 'new':
                    db_obj['status'] = 'active'
                else:
                    raise JSONAPIError(403, [{'token': 'This user does not exist, is already confirmed, or the token is no longer valid'}])  # noqa: 501
        except aio_exc.NotFoundError:
            raise JSONAPIError(403, [{'token': 'This user does not exist, is already confirmed, or the token is no longer valid'}])  # noqa: 501

    async def delete(self: 'LoginHandler') -> None:
        """Handle a logout request."""
        if 'X-Toja-Auth' in self.request.headers:
            try:
                user_id, token = self.request.headers['X-Toja-Auth'].split('$$')
                async with couchdb() as session:
                    db = await session['users']
                    user = await db[user_id]
                    if user and user['token'] == token:
                        user['token'] = None
                        await user.save()
            except ValueError:
                pass
            except aio_exc.NotFoundError:
                pass
        self.set_status(204)
