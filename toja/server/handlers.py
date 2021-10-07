"""API Handlers."""
import json
import logging
import traceback
from uuid import uuid1

from importlib import resources
from importlib.abc import Traversable
from io import StringIO
from mimetypes import guess_type
from tornado.web import RequestHandler

from ..models import Base
from ..validation import ValidationError
from ..utils import config, couchdb


logger = logging.getLogger(__name__)


class JSONAPIHandler(RequestHandler):
    """Base object for JSONAPI request handling."""

    def write_error(self: 'JSONAPIHandler', status_code: int, **kwargs: dict) -> None:
        """Write an error message."""
        if 'errors' in kwargs:
            self.write({'errors': kwargs['errors']})
        else:
            error = {
                'status': status_code,
            }
            if 'reason' in kwargs:
                error['detail'] = kwargs['reason']
            if 'exc_info' in kwargs:
                error_type, error_instance, tb = kwargs['exc_info']
                error['title'] = error_type.__name__
                if config()['debug']:
                    buffer = StringIO()
                    traceback.print_tb(tb, file=buffer)
                    error['detail'] = f'{str(error_instance)}\n\n{buffer.getvalue()}'
                else:
                    error['detail'] = str(error_instance)
                logger.exception(tb)
            self.write({'errors': [error]})


class CollectionHandler(JSONAPIHandler):
    """Handler for JSONAPI Collections."""

    def initialize(self: 'CollectionHandler', type: Base) -> None:
        """Initialise the handler."""
        super().initialize()
        self._type = type

    async def post(self: 'CollectionHandler') -> None:
        """Create a new JSONAPI item."""
        try:
            async with couchdb() as session:
                db = await session[self._type.name]
                obj = self._type.from_jsonapi(self._type.validate_create(json.loads(self.request.body)['data']))
                await obj.check_unique(db)
                await obj.pre_create(db)
                db_obj = await db.create(str(uuid1()))
                db_obj.update(obj.as_couchdb())
                await db_obj.save()
                obj._id = db_obj['_id']
                await obj.post_create(db)
                try:
                    await obj.check_unique(db)
                except ValidationError as ve:
                    await db_obj.delete()
                    raise ve
                self.write({'data': obj.as_jsonapi()})
        except ValidationError as ve:
            self.send_error(400, errors=ve.errors)


class ItemHandler(JSONAPIHandler):
    """Handler for an individual JSONAPI item."""

    def initialize(self: 'ItemHandler', type: Base) -> None:
        """Initialise the handler."""
        super().initialize()
        self._type = type

    async def get(self: 'ItemHandler', identifier: str) -> None:
        """Fetch a single item."""
        pass
        '''session = get_session(self._config)
        try:
            result = await session.query(self._type).single(identifier)
            self.write({'data': result.as_jsonapi()})
        except NotFoundError:
            self.send_error(404, reason=f'{self._type.__name__} {identifier} not found')'''


class FrontendHandler(RequestHandler):
    """Handler for the frontend application files."""

    def get(self: 'FrontendHandler', path: str) -> None:
        """Get the file at the given path.

        :param path: The path to get.
        :type: path: str
        """
        self.xsrf_token
        if not path.strip():
            path = '/'
        base = resources.files('toja')
        public = base / 'server' / 'frontend' / 'public'
        try:
            logger.debug(f'Attempting to send {path}')
            self._get_resource(public, path.split('/')[1:])
        except FileNotFoundError:
            logger.debug('Sending index.html')
            self._get_resource(public, ('index.html', ))

    def _get_resource(self: 'FrontendHandler', resource: Traversable, path: list[str]) -> None:
        """Send a file.

        Performs mimetype guessing and sets the appropriate Content-Type header.

        :param resource: The root resource to serve files from
        :type resource: importlib.Traversable
        :param path: The path to the file to send
        :type path: list[str]
        """
        for part in path:
            resource = resource / part
        try:
            data = resource.read_bytes()
            mimetype = guess_type(path[-1])
            if mimetype:
                self.set_header('Content-Type', mimetype[0])
            self.write(data)
        except IsADirectoryError:
            raise FileNotFoundError()
