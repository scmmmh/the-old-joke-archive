"""API Handlers."""
import json
import logging
import traceback

from io import StringIO
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
