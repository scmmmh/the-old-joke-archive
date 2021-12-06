"""Handler for test setup requests."""
from tornado.web import RequestHandler

from toja.setup import setup_backend, reset_backend


class TestHandler(RequestHandler):
    """Handler to create and delete the backend storage."""

    async def post(self: 'TestHandler') -> None:
        """Create the backend setup."""
        await setup_backend()

    async def delete(self: 'TestHandler') -> None:
        """Delete the backend setup."""
        await reset_backend()

    def check_xsrf_cookie(self: 'TestHandler') -> None:
        """No XSRF cookie support needed."""
        return False
