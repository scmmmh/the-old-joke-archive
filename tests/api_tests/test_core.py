"""Basic tests to check that the API can handle fundamentally invalid requests."""
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError


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
