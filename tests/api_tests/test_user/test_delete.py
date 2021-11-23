"""Tests for user access."""
import json
import pytest

from aiocouch import CouchDB, exception as aio_exc
from tornado.httpclient import HTTPClientError
from typing import Tuple


@pytest.mark.asyncio
async def test_delete_self(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting the user itself works."""
    db, users = standard_database
    response = await http_client['delete'](f'/api/users/{users["user1"]["_id"]}',
                                           token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert response.code == 204
    with pytest.raises(aio_exc.NotFoundError):
        await (await db['users'])[users['user1']['_id']]


@pytest.mark.asyncio
async def test_delete_by_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a user by an admin works."""
    db, users = standard_database
    response = await http_client['delete'](f'/api/users/{users["user1"]["_id"]}',
                                           token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert response.code == 204
    with pytest.raises(aio_exc.NotFoundError):
        await (await db['users'])[users['user1']['_id']]


@pytest.mark.asyncio
async def test_fail_incorrect_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a non-existant user fails."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete']('/api/users/does-not-exist',
                                    token=f'{users["admin"]["_id"]}$${users["admin"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_delete_by_non_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a user by a non-admin does not work."""
    session, users = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete'](f'/api/users/{users["admin"]["_id"]}',
                                    token=f'{users["user1"]["_id"]}$${users["user1"]["tokens"][0]["token"]}')
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
