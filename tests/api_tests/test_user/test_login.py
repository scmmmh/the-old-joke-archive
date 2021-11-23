"""Tests for user login."""
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import AsyncGenerator, Tuple


async def async_gen_to_list(generator: AsyncGenerator) -> list:
    """Transform the values of an async generator into a list."""
    items = []
    async for item in generator:
        items.append(item)
    return items


@pytest.mark.asyncio
async def test_login(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 1 works."""
    db, users = standard_database
    users_db = await db['users']
    user = (await async_gen_to_list(users_db.find({'email': 'admin@example.com'})))[0]
    token = user['tokens'][0]['token']
    response = await http_client['post']('/api/users/_login',
                                         {'type': 'users',
                                          'attributes': {'email': 'admin@example.com',
                                                         'password': 'admin1pwd'}})
    assert response.code == 200
    user = (await async_gen_to_list(users_db.find({'email': 'admin@example.com'})))[0]
    assert token != user['tokens'][0]['token']


@pytest.mark.asyncio
async def test_fail_login_missing_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login fails for a missing e-mail address."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {}})
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_fail_login_invalid_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login fails for an incorrect e-mail address."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'email': 'does-not-exist@example.com',
                                                  'password': 'invalid'}})
    assert exc_info.value.code == 403


@pytest.mark.asyncio
async def test_fail_login_invalid_password(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login fails for an invalid password."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'email': 'admin@example.com',
                                                  'password': 'invalid'}})
    assert exc_info.value.code == 403
