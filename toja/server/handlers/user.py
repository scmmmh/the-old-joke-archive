"""User-related request handlers."""
from aiocouch import Document, exception as aio_exc

from secrets import token_hex
from typing import Union
from urllib.parse import urlencode

from toja.utils import couchdb, send_email, config, JSONAPIError
from toja.validation import validate, ValidationError
from uuid import uuid1
from .base import JSONAPIHandler, JSONAPICollectionHandler, JSONAPIItemHandler


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
        }
        if user and ('admin' in user['groups'] or 'admin:user' in user['groups']):
            schema['attributes']['schema']['groups'] = {
                'type': 'list',
                'schema': {
                    'type': 'string'
                }
            }
        obj = validate(schema, data)
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
                async with Document(db, iid) as doc:
                    doc['email'] = data['attributes']['email']
                    doc['name'] = data['attributes']['name']
                    if 'groups' in data['attributes']:
                        doc['groups'] = data['attributes']['groups']
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
                    'token': {
                        'type': 'string',
                        'required': False,
                        'empty': False,
                    },
                    'remember': {
                        'type': 'boolean',
                        'required': False,
                        'empty': False,
                        'default': False,
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
                if 'token' in user['attributes']:
                    db_obj = None
                    async for tmp in db.find({'email': user['attributes']['email'],
                                              'token': user['attributes']['token']}):
                        db_obj = tmp
                    if db_obj is None:
                        raise JSONAPIError(403, [{'title': 'This e-mail address is not registered or the token is no longer valid'}])  # noqa: 501
                    self.set_status(200)
                    self.write({
                        'data': {
                            'type': 'users',
                            'id': db_obj['_id'],
                        }
                    })
                else:
                    db_obj = None
                    async for tmp in db.find({'email': user['attributes']['email']}):
                        db_obj = tmp
                    if db_obj is None:
                        raise JSONAPIError(403, [{'title': 'This e-mail address is not registered or the token is no longer valid'}])  # noqa: 501
                    else:
                        db_obj['token'] = token_hex(128)
                        await db_obj.save()
                        send_email(db_obj['email'], 'Log in to The Old Joke Archive', f'''Hello {db_obj["name"]},

Please use the following link to log into The Old Joke Archive:

{config()['server']['base']}/app/user/log-in?{urlencode((('email', db_obj['email']), ('token', db_obj['token']), ('remember', user['attributes']['remember'])))}

The Old Joke Automaton.
''')  # noqa: E501
                        self.set_status(204)
        except aio_exc.NotFoundError:
            raise JSONAPIError(403,
                               [{'title': 'This e-mail address is not registered or the token is no longer valid'}])
        '''try:
            async with couchdb() as session:
                db = await session['users']
                obj = User.from_jsonapi(User.validate_login(json.loads(self.request.body)['data']))
                remember = obj._attributes['remember']
                if 'token' in obj._attributes:
                    db_obj = None
                    async for user in db.find({'email': obj._attributes['email'], 'token': obj._attributes['token']}):
                        db_obj = user
                    if db_obj is None:
                        self.send_error(403, errors=[{
                            'code': 403,
                            'title': 'This e-mail address is not registered or the token is no longer valid'
                        }])
                    else:
                        obj = User.from_couchdb(db_obj)
                        self.write({'data': obj.as_jsonapi()})
                else:
                    db_obj = None
                    async for user in db.find({'email': obj._attributes['email']}):
                        db_obj = user
                    if db_obj is None:
                        self.send_error(403, errors=[{
                            'code': 403,
                            'title': 'This e-mail address is not registered or your account has been blocked'
                        }])
                    else:
                        db_obj['token'] = token_hex(128)
                        await db_obj.save()
                        obj = User.from_couchdb(db_obj)
                        await obj.send_login_email(remember='true' if remember else 'false')
                        self.set_status(204)
        except ValidationError as ve:
            self.send_error(400, errors=ve.errors)'''

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
