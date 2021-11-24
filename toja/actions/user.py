"""Actions related to the user."""
import logging

from datetime import datetime

from ..utils import couchdb


logger = logging.getLogger(__name__)


async def clean_old_user_tokens() -> None:
    """Clean out tokens over 30 days old."""
    logger.debug('Cleaning old user tokens')
    limit = datetime.utcnow().timestamp()
    async with couchdb() as session:
        db = await session['users']
        async for user in db.docs():
            if 'tokens' in user and isinstance(user['tokens'], list):
                filtered_tokens = []
                for token in user['tokens']:
                    if token['timestamp'] is not None:
                        if token['timestamp'] >= limit:
                            filtered_tokens.append(token)
                user['tokens'] = filtered_tokens
                await user.save()
    logger.debug('Old user tokens cleaned out')
