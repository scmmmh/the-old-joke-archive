"""Tests for user access."""
import json
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple


@pytest.mark.asyncio
async def test_get_self(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that accessing the user's own data works for admins."""
    db, users = standard_database
    response = await http_client['get'](f'/api/users/{users["admin"]["_id"]}',
                                        token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users = await db['users']
    db_user = await users[user['id']]
    assert user is not None
    assert 'attributes' in user
    assert 'email' in user['attributes']
    assert 'name' in user['attributes']
    assert 'groups' in user['attributes']
    assert db_user
    assert db_user['email'] == user['attributes']['email']
    assert db_user['name'] == user['attributes']['name']
    assert db_user['groups'] == user['attributes']['groups']


@pytest.mark.asyncio
async def test_get_self_non_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that accessing the user's own data works for non-admins."""
    db, users = standard_database
    response = await http_client['get'](f'/api/users/{users["user1"]["_id"]}',
                                        token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users = await db['users']
    db_user = await users[user['id']]
    assert user is not None
    assert 'attributes' in user
    assert 'email' in user['attributes']
    assert 'name' in user['attributes']
    assert 'groups' in user['attributes']
    assert db_user
    assert db_user['email'] == user['attributes']['email']
    assert db_user['name'] == user['attributes']['name']
    assert db_user['groups'] == user['attributes']['groups']


@pytest.mark.asyncio
async def test_get_other_by_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that accessing the another user's data works for admins."""
    db, users = standard_database
    response = await http_client['get'](f'/api/users/{users["user1"]["_id"]}',
                                        token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users = await db['users']
    db_user = await users[user['id']]
    assert user is not None
    assert 'attributes' in user
    assert 'email' in user['attributes']
    assert 'name' in user['attributes']
    assert 'groups' in user['attributes']
    assert db_user
    assert db_user['email'] == user['attributes']['email']
    assert db_user['name'] == user['attributes']['name']
    assert db_user['groups'] == user['attributes']['groups']


@pytest.mark.asyncio
async def test_fail_incorrect_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that fetching a non-existant user fails."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['get']('/api/users/does-not-exist',
                                 token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_get_other_user_by_non_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that fetching another user by a non-admin fails."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['get'](f'/api/users/{users["admin"]["_id"]}',
                                 token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
