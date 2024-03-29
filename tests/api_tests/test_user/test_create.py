"""Tests for user creation."""
import json
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple


@pytest.mark.asyncio
async def test_create_first_user(empty_database: CouchDB, http_client: dict) -> None:
    """Test that creating the first user works."""
    response = await http_client['post']('/api/users',
                                         body={'type': 'users',
                                               'attributes': {'email': 'test@oldjokearchive.com',
                                                              'name': 'A Tester'}})
    assert response.code == 201
    user = json.load(response.buffer)['data']
    assert user
    assert 'admin' in user['attributes']['groups']
    db_user = await (await empty_database['users'])[user['id']]
    assert db_user
    assert db_user['status'] == 'new'
    assert 'password' not in db_user
    user['attributes']['password'] = 'blabla'
    response = await http_client['put'](f'/api/users/{user["id"]}',
                                        token=f'{user["id"]}$${db_user["tokens"][0]["token"]}',
                                        body=user)
    user = json.load(response.buffer)['data']
    assert user
    db_user = await (await empty_database['users'])[user['id']]
    assert db_user
    assert db_user['status'] == 'active'
    assert 'password' in db_user


@pytest.mark.asyncio
async def test_create_second_user(minimal_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a further user does not give admin privileges."""
    session, _ = minimal_database
    response = await http_client['post']('/api/users',
                                         body={'type': 'users',
                                               'attributes': {'email': 'test@oldjokearchive.com',
                                                              'name': 'A Tester'}})
    assert response.code == 201
    user = json.load(response.buffer)['data']
    assert user
    assert 'admin' not in user['attributes']['groups']
    db_user = await (await session['users'])[user['id']]
    assert db_user
    assert db_user['status'] == 'new'
    assert 'password' not in db_user
    user['attributes']['password'] = 'blabla'
    response = await http_client['put'](f'/api/users/{user["id"]}',
                                        token=f'{user["id"]}$${db_user["tokens"][0]["token"]}',
                                        body=user)
    user = json.load(response.buffer)['data']
    assert user
    db_user = await (await session['users'])[user['id']]
    assert db_user
    assert db_user['status'] == 'active'
    assert 'password' in db_user


@pytest.mark.asyncio
async def test_fail_create_no_name(minimal_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a with no name fails."""
    session, _ = minimal_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users',
                                  body={'type': 'users',
                                        'attributes': {'email': 'test@oldjokearchive.com'}})
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_create_empty_name(minimal_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a with an empty name fails."""
    session, _ = minimal_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users',
                                  body={'type': 'users',
                                        'attributes': {'email': 'test@oldjokearchive.com',
                                                       'name': ''}})
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_create_no_email(minimal_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a with no email fails."""
    session, _ = minimal_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users',
                                  body={'type': 'users',
                                        'attributes': {'name': 'A Tester'}})
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_create_empty_email(minimal_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a with an empty email fails."""
    session, _ = minimal_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users',
                                  body={'type': 'users',
                                        'attributes': {'email': '',
                                                       'name': 'A Tester'}})
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_create_additional_data(minimal_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a with additional fields fails."""
    session, _ = minimal_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users',
                                  body={'type': 'users',
                                        'attributes': {'email': 'test@oldjokearchive.com',
                                                       'name': 'A Tester',
                                                       'token': 'hack',
                                                       'groups': ['admin']}})
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
