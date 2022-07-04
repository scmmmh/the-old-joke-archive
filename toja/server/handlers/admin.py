"""Admin functionality handlers."""
from .base import BaseHandler

from ...utils import mosquitto


class AdminSearchHandler(BaseHandler):
    """Handles administrative actions for the search system."""

    async def post(self: 'AdminSearchHandler') -> None:
        """Handle a post request, starting the requested action."""
        action = self.json_body()
        user = await self.get_user()
        if user and 'admin' in user['groups']:
            if action['action'] == 're-index':
                async with mosquitto() as client:
                    await client.publish('admin/search/re-index')
                self.set_status(202)
