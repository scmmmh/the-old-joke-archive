"""API Handlers."""
from aiocouch import exception
from tornado.web import RequestHandler

from ..models import connect_database


class CollectionHandler(RequestHandler):
    """Handler for JSONAPI Collections."""

    def initialize(self, config: dict, type: str) -> None:  # noqa: ANN101
        """Initialise the handler."""
        self._config = config
        self._type = type


class ItemHandler(RequestHandler):
    """Handler for an individual JSONAPI Item."""

    def initialize(self, config: dict, type: str) -> None:  # noqa: ANN101
        """Initialise the handler."""
        self._config = config
        self._type = type

    async def get(self, identifier: str) -> None:  # noqa: ANN101
        """Fetch a single item."""
        async with connect_database(self._config) as session:
            try:
                db = await session[self._type]
                item = await db[identifier]
                self.write(item)
            except exception.NotFoundError:
                self.send_error(404)
