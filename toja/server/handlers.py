"""API Handlers."""
import json
import logging
import traceback

from importlib import resources
from io import StringIO
from mimetypes import guess_type
from tornado.web import RequestHandler

from ..models import get_session, NotFoundError


logger = logging.getLogger(__name__)


class JSONAPIHandler(RequestHandler):
    """Base object for JSONAPI request handling."""

    def initialize(self, config: dict) -> None:  # noqa: ANN101
        """Initialize the handler."""
        self._config = config

    def write_error(self, status_code: int, **kwargs: dict) -> None:  # noqa: ANN101
        """Write an error message."""
        error = {
            'status': status_code,
        }
        if 'reason' in kwargs:
            error['detail'] = kwargs['reason']
        if 'exc_info' in kwargs:
            error_type, error_instance, tb = kwargs['exc_info']
            error['title'] = error_type.__name__
            if self._config['debug']:
                buffer = StringIO()
                traceback.print_tb(tb, file=buffer)
                error['detail'] = f'{str(error_instance)}\n\n{buffer.getvalue()}'
            else:
                error['detail'] = str(error_instance)
            logger.exception(tb)

        self.write({'errors': [error]})


class CollectionHandler(JSONAPIHandler):
    """Handler for JSONAPI Collections."""

    def initialize(self, config: dict, type: str) -> None:  # noqa: ANN101
        """Initialise the handler."""
        super().initialize(config)
        self._type = type

    async def post(self: 'CollectionHandler') -> None:
        """Create a new individual JSONAPI item."""
        session = get_session(self._config)
        result = await session.query(self._type).create(self._type().from_jsonapi(json.loads(self.request.body)))
        self.write(result.as_jsonapi())


class ItemHandler(JSONAPIHandler):
    """Handler for an individual JSONAPI item."""

    def initialize(self, config: dict, type: str) -> None:  # noqa: ANN101
        """Initialise the handler."""
        super().initialize(config)
        self._type = type

    async def get(self, identifier: str) -> None:  # noqa: ANN101
        """Fetch a single item."""
        session = get_session(self._config)
        try:
            result = await session.query(self._type).single(identifier)
            self.write({'data': result.as_jsonapi()})
        except NotFoundError:
            self.send_error(404, reason=f'{self._type.__name__} {identifier} not found')


class FrontendHandler(RequestHandler):
    """Handler for the frontend application files."""

    def get(self: 'FrontendHandler', path: str) -> None:
        """Get the file at the given path.

        :param path: The path to get.
        :type: path: str
        """
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

    def _get_resource(self: 'FrontendHandler', resource: resources.Traversable, path: list[str]) -> None:
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
