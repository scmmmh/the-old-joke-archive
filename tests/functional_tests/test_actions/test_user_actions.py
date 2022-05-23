"""Tests for user actions."""
import pytest

from aiocouch import CouchDB
from datetime import datetime, timedelta

from toja.actions import clean_old_user_tokens


@pytest.mark.asyncio
async def test_clean_old_user_tokens(standard_database: CouchDB) -> None:
    """Test that old tokens are removed correctly."""
    db, users = standard_database
    users_db = await db['users']
    admin = await users_db[users['admin']['_id']]
    assert len(admin['tokens']) == 1
    admin['tokens'][0]['timestamp'] = (datetime.utcnow() - timedelta(days=1)).timestamp()
    admin['tokens'].append({
        'token': '',
        'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()
    })
    await admin.save()
    await clean_old_user_tokens()
    admin = await users_db[users['admin']['_id']]
    assert len(admin['tokens']) == 1
    assert admin['tokens'][0]['timestamp'] >= datetime.utcnow().timestamp()
