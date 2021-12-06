"""Tests for user editing."""
import json
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple


@pytest.mark.asyncio
async def test_update_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating the admin user works."""
    db, users = standard_database
    response = await http_client['put'](f'/api/users/{users["admin"]["_id"]}',
                                        body={'type': 'users',
                                              'id': users['admin']['_id'],
                                              'attributes': {'email': 'admin1@example.com',
                                                             'name': 'The Best Admin',
                                                             'groups': ['admin', 'new-group']}},
                                        token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users = await db['users']
    db_user = await users[user['id']]
    assert db_user
    assert db_user['email'] == 'admin1@example.com'
    assert db_user['name'] == 'The Best Admin'
    assert db_user['groups'] == ['admin', 'new-group']


@pytest.mark.asyncio
async def test_update_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a user works."""
    db, users = standard_database
    response = await http_client['put'](f'/api/users/{users["user1"]["_id"]}',
                                        body={'type': 'users',
                                              'id': users['user1']['_id'],
                                              'attributes': {'email': 'user_one@example.com',
                                                             'name': 'User Eins'}},
                                        token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users = await db['users']
    db_user = await users[user['id']]
    assert db_user
    assert db_user['email'] == 'user_one@example.com'
    assert db_user['name'] == 'User Eins'
    assert db_user['groups'] == []


@pytest.mark.asyncio
async def test_update_user_only_name(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a user works when only updating the name."""
    db, users = standard_database
    response = await http_client['put'](f'/api/users/{users["user1"]["_id"]}',
                                        body={'type': 'users',
                                              'id': users['user1']['_id'],
                                              'attributes': {'name': 'User Eins'}},
                                        token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users = await db['users']
    db_user = await users[user['id']]
    assert db_user
    assert db_user['email'] == 'user1@example.com'
    assert db_user['name'] == 'User Eins'
    assert db_user['groups'] == []


@pytest.mark.asyncio
async def test_fail_nonexistent_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a non-existent id fails."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put']('/api/users/abc',
                                 body={'type': 'users',
                                       'id': 'abc',
                                       'attributes': {'email': 'test@example.com',
                                                      'name': 'User One'}},
                                 token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_incorrect_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with an incorrect id fails."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{users["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': 'something',
                                       'attributes': {'email': 'test@example.com',
                                                      'name': 'User One'}},
                                 token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_non_admin_update_groups(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating the groups of a user does not work for non-admins."""
    session, users = standard_database
    response = await http_client['put'](f'/api/users/{users["user1"]["_id"]}',
                                        body={'type': 'users',
                                              'id': users['user1']['_id'],
                                              'attributes': {'email': 'user@example.com',
                                                             'name': 'User One',
                                                             'groups': ['admin']}},
                                        token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    user = json.load(response.buffer)['data']
    users = await session['users']
    db_user = await users[user['id']]
    assert db_user['groups'] == []


@pytest.mark.asyncio
async def test_fail_non_admin_update_not_self(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that a non-admin user can only update themselves."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{users["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': users['admin']['_id'],
                                       'attributes': {'email': 'admin1@example.com',
                                                      'name': 'The Best Admin'}},
                                 token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_update_to_existing_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that a non-admin user can only update themselves."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{users["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': users['admin']['_id'],
                                       'attributes': {'email': 'user1@example.com',
                                                      'name': 'The Best Admin'}},
                                 token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_update_additional_fields(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with additional fields fails."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{users["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': users['admin']['_id'],
                                       'attributes': {'email': 'user1@example.com',
                                                      'name': 'The Best Admin',
                                                      'token': '123456'}},
                                 token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
