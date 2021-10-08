"""Tests for user creation."""
import json
import pytest

from aiocouch import CouchDB
from typing import Tuple


@pytest.mark.asyncio
async def test_create_first_user(empty_database: CouchDB, http_client: dict) -> None:
    """Test that creating the first user works."""
    response = await http_client['post']('/api/users',
                                         body={'type': 'users',
                                               'attributes': {'email': 'test@example.com',
                                                              'name': 'A Tester'}})
    assert response.code == 201
    user = json.load(response.buffer)['data']
    assert await (await empty_database['users'])[user['id']]
    assert 'admin' in user['attributes']['groups']


@pytest.mark.asyncio
async def test_create_second_user(default_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a further user does not give admin privileges."""
    session, _ = default_database
    response = await http_client['post']('/api/users',
                                         body={'type': 'users',
                                               'attributes': {'email': 'test@example.com',
                                                              'name': 'A Tester'}})
    assert response.code == 201
    user = json.load(response.buffer)['data']
    assert await (await session['users'])[user['id']]
    assert 'admin' not in user['attributes']['groups']
