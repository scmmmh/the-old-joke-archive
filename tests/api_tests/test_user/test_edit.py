"""Tests for user editing."""
import json
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_update_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating the admin user works."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                        body={'type': 'users',
                                              'id': objs['users']['admin']['_id'],
                                              'attributes': {'email': 'admin1@oldjokearchive.com',
                                                             'name': 'The Best Admin',
                                                             'groups': ['admin', 'new-group']}},
                                        token=auth_token(objs['users']['admin']))
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users_db = await session['users']
    db_user = await users_db[user['id']]
    assert db_user
    assert db_user['email'] == 'admin1@oldjokearchive.com'
    assert db_user['name'] == 'The Best Admin'
    assert db_user['groups'] == ['admin', 'new-group']


@pytest.mark.asyncio
async def test_update_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a user works."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/users/{objs["users"]["one"]["_id"]}',
                                        body={'type': 'users',
                                              'id': objs['users']['one']['_id'],
                                              'attributes': {'email': 'user_one@oldjokearchive.com',
                                                             'name': 'User Eins'}},
                                        token=auth_token(objs['users']['one']))
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users_db = await session['users']
    db_user = await users_db[user['id']]
    assert db_user
    assert db_user['email'] == 'user_one@oldjokearchive.com'
    assert db_user['name'] == 'User Eins'
    assert db_user['groups'] == []


@pytest.mark.asyncio
async def test_update_user_only_name(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a user works when only updating the name."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/users/{objs["users"]["one"]["_id"]}',
                                        body={'type': 'users',
                                              'id': objs['users']['one']['_id'],
                                              'attributes': {'name': 'User Eins'}},
                                        token=auth_token(objs['users']['one']))
    assert response.code == 200
    user = json.load(response.buffer)['data']
    users_db = await session['users']
    db_user = await users_db[user['id']]
    assert db_user
    assert db_user['email'] == 'user1@oldjokearchive.com'
    assert db_user['name'] == 'User Eins'
    assert db_user['groups'] == []


@pytest.mark.asyncio
async def test_fail_nonexistent_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a non-existent id fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put']('/api/users/abc',
                                 body={'type': 'users',
                                       'id': 'abc',
                                       'attributes': {'email': 'test@oldjokearchive.com',
                                                      'name': 'User One'}},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_incorrect_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with an incorrect id fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': 'something',
                                       'attributes': {'email': 'test@oldjokearchive.com',
                                                      'name': 'User One'}},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_non_admin_update_groups(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating the groups of a user does not work for non-admins."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/users/{objs["users"]["one"]["_id"]}',
                                        body={'type': 'users',
                                              'id': objs['users']['one']['_id'],
                                              'attributes': {'email': 'user@oldjokearchive.com',
                                                             'name': 'User One',
                                                             'groups': ['admin']}},
                                        token=auth_token(objs['users']['one']))
    user = json.load(response.buffer)['data']
    users_db = await session['users']
    db_user = await users_db[user['id']]
    assert db_user['groups'] == []


@pytest.mark.asyncio
async def test_fail_non_admin_update_not_self(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that a non-admin user can only update themselves."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': objs['users']['admin']['_id'],
                                       'attributes': {'email': 'admin1@oldjokearchive.com',
                                                      'name': 'The Best Admin'}},
                                 token=auth_token(objs['users']['one']))
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_update_to_existing_email(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that a non-admin user can only update themselves."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': objs['users']['admin']['_id'],
                                       'attributes': {'email': 'user1@oldjokearchive.com',
                                                      'name': 'The Best Admin'}},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_update_additional_fields(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with additional fields fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                 body={'type': 'users',
                                       'id': objs['users']['admin']['_id'],
                                       'attributes': {'email': 'user1@oldjokearchive.com',
                                                      'name': 'The Best Admin',
                                                      'token': '123456'}},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
