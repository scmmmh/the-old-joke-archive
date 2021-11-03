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
async def test_login_step_1(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 1 works."""
    db, users = standard_database
    users_db = await db['users']
    user = (await async_gen_to_list(users_db.find({'email': 'admin@example.com'})))[0]
    token = user['token']
    response = await http_client['post']('/api/users/_login',
                                         {'type': 'users',
                                          'attributes': {'email': 'admin@example.com'}})
    assert response.code == 204
    user = (await async_gen_to_list(users_db.find({'email': 'admin@example.com'})))[0]
    assert token != user['token']


@pytest.mark.asyncio
async def test_login_step_2(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 2 works."""
    db, users = standard_database
    response = await http_client['post']('/api/users/_login',
                                         {'type': 'users',
                                          'attributes': {'email': 'admin@example.com',
                                                         'token': users['admin']['token']}})
    assert response.code == 200


@pytest.mark.asyncio
async def test_fail_login_step_1_missing_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 1 fails for a missing e-mail address."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {}})
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_fail_login_step_1_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 1 fails for an incorrect e-mail address."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'email': 'does-not-exist@example.com'}})
    assert exc_info.value.code == 403


@pytest.mark.asyncio
async def test_fail_login_step_2_validation_missing_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:  # noqa: E501
    """Test that the login step 2 fails for a missing e-mail address."""
    db, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'token': users['admin']['token']}})
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_fail_login_step_2_incorrect_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 2 fails for an invalid e-mail address."""
    db, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'email': 'does-not-exist@example.com',
                                                  'token': users['admin']['token']}})
    assert exc_info.value.code == 403


@pytest.mark.asyncio
async def test_fail_login_step_2_incorrect_token(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login step 2 fails for an incorrect token."""
    db, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'email': 'admin@example.com',
                                                  'token': users['user1']['token']}})
    assert exc_info.value.code == 403
