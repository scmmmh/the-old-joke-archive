"""Tests for user password reset."""
import pytest

from aiocouch import CouchDB
from typing import AsyncGenerator, Tuple


async def async_gen_to_list(generator: AsyncGenerator) -> list:
    """Transform the values of an async generator into a list."""
    items = []
    async for item in generator:
        items.append(item)
    return items


@pytest.mark.asyncio
async def test_reset_password(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the password reset step works."""
    session, objs = standard_database
    users_db = await session['users']
    user = (await async_gen_to_list(users_db.find({'email': 'admin@oldjokearchive.com'})))[0]
    token = user['tokens'][0]['token']
    response = await http_client['post']('/api/users/_reset-password',
                                         {'type': 'users',
                                          'attributes': {'email': 'admin@oldjokearchive.com'}})
    assert response.code == 204
    user = (await async_gen_to_list(users_db.find({'email': 'admin@oldjokearchive.com'})))[0]
    assert token != user['tokens'][0]['token']
