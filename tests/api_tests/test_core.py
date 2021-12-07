"""Basic tests to check that the API can handle fundamentally invalid requests."""
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple


@pytest.mark.asyncio
async def test_handle_create_empty_body(empty_database: CouchDB, http_client: dict) -> None:
    """Test that an empty create body is handled correctly."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users', body='')
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_handle_create_empty_object(empty_database: CouchDB, http_client: dict) -> None:
    """Test that an empty object in the create body is handled correctly."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users', body='{}')
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_handle_create_empty_data_object(empty_database: CouchDB, http_client: dict) -> None:
    """Test that an empty data object in the create body is handled correctly."""
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/users', body='{"data": ""}')
    assert exc_info.value.code == 400


@pytest.mark.asyncio
async def test_access_time_updated(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that accessing the api updates the last_access timestamp."""
    db, objs = standard_database
    response = await http_client['get'](f'/api/users/{objs["users"]["admin"]["_id"]}',
                                        token=f'{objs["users"]["admin"]["_id"]}$${objs["users"]["admin"]["tokens"][0]["token"]}')  # noqa: E501
    assert response.code == 200
    users_db = await db['users']
    db_user = await users_db[objs['users']['admin']['_id']]
    assert db_user is not None
    assert 'last_access' in db_user
    assert db_user['last_access'] > 0
    assert db_user['last_access'] != objs['users']['admin']['last_access']
