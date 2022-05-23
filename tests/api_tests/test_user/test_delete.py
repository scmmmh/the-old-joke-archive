"""Tests for user access."""
import json
import pytest

from aiocouch import CouchDB, exception as aio_exc
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_delete_self(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting the user itself works."""
    session, objs = standard_database
    response = await http_client['delete'](f'/api/users/{objs["users"]["one"]["_id"]}',
                                           token=auth_token(objs['users']['one']))
    assert response.code == 204
    with pytest.raises(aio_exc.NotFoundError):
        await (await session['users'])[objs['users']['one']['_id']]


@pytest.mark.asyncio
async def test_delete_by_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a user by an admin works."""
    session, objs = standard_database
    response = await http_client['delete'](f'/api/users/{objs["users"]["one"]["_id"]}',
                                           token=auth_token(objs['users']['admin']))
    assert response.code == 204
    with pytest.raises(aio_exc.NotFoundError):
        await (await session['users'])[objs['users']['one']['_id']]


@pytest.mark.asyncio
async def test_fail_incorrect_id(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a non-existant user fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete']('/api/users/does-not-exist',
                                    token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_delete_by_non_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a user by a non-admin does not work."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                    token=auth_token(objs['users']['one']))
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
