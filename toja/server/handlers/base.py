"""Base classes for JSONAPI requests."""
import json
import logging
import traceback

from aiocouch import Document, exception as aio_exc
from io import StringIO
from tornado.web import RequestHandler
from typing import Union

from toja.validation import validate
from toja.utils import couchdb, JSONAPIError, config


logger = logging.getLogger(__name__)


class JSONAPIHandler(RequestHandler):
    """Base class for all JSONAPI requests."""

    jsonapi_body_schema = {
        'data': {
            'type': 'dict',
            'required': True,
            'empty': False,
        }
    }

    async def get_user(self: 'JSONAPIHandler') -> Union[Document, None]:
        """Get the current user based on the X-Toja-Auth header."""
        if 'X-Toja-Auth' in self.request.headers:
            try:
                user_id, token = self.request.headers['X-Toja-Auth'].split('$$')
                async with couchdb() as session:
                    db = await session['users']
                    user = await db[user_id]
                    for user_token in user['tokens']:
                        if user_token['token'] == token:
                            return user
            except ValueError:
                pass
            except aio_exc.NotFoundError:
                pass
        return None

    async def jsonapi_body(self: 'JSONAPIHandler') -> None:
        """Get the JSON body.

        Raises JSONAPIError if it isn't a valid JSONAPI body.
        """
        try:
            body = json.loads(self.request.body)
            return validate(self.jsonapi_body_schema, body)['data']
        except json.JSONDecodeError:
            raise JSONAPIError(400, [{'title': 'The request body must be valid JSON.'}])

    def write_error(self: 'JSONAPIHandler', status_code: int, **kwargs: dict) -> None:
        """Write an error message."""
        error_type, error_instance, tb = kwargs['exc_info']
        if isinstance(error_instance, JSONAPIError):
            if config()['debug']:
                logger.exception(tb)
            self.set_status(error_instance.status_code)
            self.write(error_instance.as_jsonapi())
        else:
            error = {}
            error['title'] = error_type.__name__
            if config()['debug']:
                buffer = StringIO()
                traceback.print_tb(tb, file=buffer)
                error['detail'] = f'{str(error_instance)}\n\n{buffer.getvalue()}'
            else:
                error['detail'] = str(error_instance)
            logger.exception('Exception', exc_info=kwargs['exc_info'])
            self.set_status(status_code)
            self.write({'errors': [error]})


class JSONAPICollectionHandler(JSONAPIHandler):
    """Base class for handling collection-level requests."""

    async def allow_post(self: 'JSONAPICollectionHandler', data: dict, user: Union[Document, None]) -> None:
        """Check whether POST requests are allowed."""
        raise JSONAPIError(403, [{'title': 'You are not authorised to create new items of this type'}])

    async def validate_post(self: 'JSONAPICollectionHandler', data: dict, user: Union[Document, None]) -> dict:
        """Validate that the POST data is valid."""
        return data

    async def create_post(self: 'JSONAPICollectionHandler', data: dict, user: Union[Document, None]) -> Document:
        """Create a new CouchDB document."""
        raise JSONAPIError(500, [{'title': 'New items of this type cannot be created'}])

    async def as_jsonapi(self: 'JSONAPICollectionHandler', doc: Document) -> dict:
        """Return a single ``doc`` in JSONAPI format."""
        return {}

    async def post(self: 'JSONAPICollectionHandler') -> None:
        """Handle POST requests."""
        user = await self.get_user()
        data = await self.jsonapi_body()
        await self.allow_post(data, user)
        obj = await self.validate_post(data, user)
        doc = await self.create_post(obj, user)
        data = await self.as_jsonapi(doc)
        self.set_status(201)
        self.write({'data': data})


class JSONAPIItemHandler(JSONAPIHandler):
    """Base class for handling item-level requests."""

    async def allow_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether GET requests are allowed."""
        raise JSONAPIError(403, [{'title': 'You are not authorised to access this item'}])

    async def create_get(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> Document:
        """Fetch a CouchDB document for a GET request."""
        raise JSONAPIError(500, [{'title': 'Items of this type cannot be updated'}])

    async def get(self: 'JSONAPIItemHandler', iid: str) -> None:
        """Handle GET requests."""
        user = await self.get_user()
        await self.allow_get(iid, user)
        doc = await self.create_get(iid, user)
        data = await self.as_jsonapi(doc)
        self.set_status(200)
        self.write({'data': data})

    async def allow_put(self: 'JSONAPIItemHandler', iid: str, data: dict, user: Union[Document, None]) -> None:
        """Check whether PUT requests are allowed."""
        raise JSONAPIError(403, [{'title': 'You are not authorised to update this item'}])

    async def validate_put(self: 'JSONAPIItemHandler', iid: str, data: dict, user: Union[Document, None]) -> dict:
        """Validate that the PUT data is valid."""
        return data

    async def create_put(self: 'JSONAPIItemHandler', iid: str, data: dict, user: Union[Document, None]) -> Document:
        """Update a CouchDB document for a PUT request."""
        raise JSONAPIError(500, [{'title': 'Items of this type cannot be updated'}])

    async def put(self: 'JSONAPIItemHandler', iid: str) -> None:
        """Handle PUT requests."""
        user = await self.get_user()
        data = await self.jsonapi_body()
        await self.allow_put(iid, data, user)
        obj = await self.validate_put(iid, data, user)
        doc = await self.create_put(iid, obj, user)
        data = await self.as_jsonapi(doc)
        self.set_status(200)
        self.write({'data': data})

    async def as_jsonapi(self: 'JSONAPIItemHandler', doc: Document) -> dict:
        """Return a single ``doc`` in JSONAPI format."""
        return {}

    async def allow_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Check whether DELETE requests are allowed."""
        raise JSONAPIError(403, [{'title': 'You are not authorised to delete this item'}])

    async def create_delete(self: 'JSONAPIItemHandler', iid: str, user: Union[Document, None]) -> None:
        """Fetch a CouchDB document for a DELETE request."""
        raise JSONAPIError(500, [{'title': 'Items of this type cannot be deleted'}])

    async def delete(self: 'JSONAPIItemHandler', iid: str) -> None:
        """Handle DELETE requests."""
        user = await self.get_user()
        await self.allow_delete(iid, user)
        await self.create_delete(iid, user)
        self.set_status(204)
