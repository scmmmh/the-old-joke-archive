"""Tests for user login."""
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple


from ..util import async_gen_to_list


@pytest.mark.asyncio
async def test_login(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login works."""
    session, objs = standard_database
    users_db = await session['users']
    user = (await async_gen_to_list(users_db.find({'email': 'admin@oldjokearchive.com'})))[0]
    token = user['tokens'][0]['token']
    response = await http_client['post']('/api/users/_login',
                                         {'type': 'users',
                                          'attributes': {'email': 'admin@oldjokearchive.com',
                                                         'password': 'adminpwd'}})
    assert response.code == 200
    user = (await async_gen_to_list(users_db.find({'email': 'admin@oldjokearchive.com'})))[0]
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
                                   'attributes': {'email': 'does-not-exist@oldjokearchive.com',
                                                  'password': 'invalid'}})
    assert exc_info.value.code == 403


@pytest.mark.asyncio
async def test_fail_login_invalid_password(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the login fails for an invalid password."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users/_login',
                                  {'type': 'users',
                                   'attributes': {'email': 'admin@oldjokearchive.com',
                                                  'password': 'invalid'}})
    assert exc_info.value.code == 403
