"""Handler for the application files."""
import logging
import re

from importlib import resources
from importlib.abc import Traversable
from mimetypes import guess_type
from tornado.web import RequestHandler


logger = logging.getLogger(__name__)


class FrontendHandler(RequestHandler):
    """Handler for the frontend application files."""

    def initialize(self: 'FrontendHandler', html_injectors: dict) -> None:
        """Initialise the frontend handler."""
        self._html_injectors = html_injectors

    async def get(self: 'FrontendHandler', path: str) -> None:
        """Get the file at the given path.

        :param path: The path to get.
        :type: path: str
        """
        self.xsrf_token
        if not path.strip():
            path = '/'
        base = resources.files('toja')
        public = base / 'server' / 'frontend' / 'dist'
        try:
            logger.debug(f'Attempting to send {path}')
            await self._get_resource(public, path.split('/')[1:])
        except FileNotFoundError:
            logger.debug('Sending index.html')
            await self._get_resource(public, ('index.html',), orig_path=path)

    async def _get_resource(
        self: 'FrontendHandler', resource: Traversable, path: list[str], orig_path: str = None
    ) -> None:  # noqa: E501
        """Send a file.

        Performs mimetype guessing and sets the appropriate Content-Type header.

        :param resource: The root resource to serve files from
        :type resource: importlib.Traversable
        :param path: The path to the file to send
        :type path: list[str]
        :param orig_path: The original path, if this is sending the default index.html
        :type orig_path: str
        """
        for part in path:
            resource = resource / part
        try:
            data = resource.read_bytes()
            if orig_path:
                for key, injector in self._html_injectors.items():
                    match = re.match(key, orig_path)
                    if match:
                        html = data.decode('utf-8')
                        split_idx = html.find('</head>')
                        html = f'{html[:split_idx]}{await injector(*match.groups())}{html[split_idx:]}'
                        data = html.encode('utf-8')
            mimetype = guess_type(path[-1])
            if mimetype:
                self.set_header('Content-Type', mimetype[0])
            self.write(data)
        except IsADirectoryError:
            raise FileNotFoundError()
