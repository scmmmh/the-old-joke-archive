"""Tests for source creation."""
import json
import pytest

from aiocouch import CouchDB
from base64 import b64decode
from io import BytesIO
from PIL import Image
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_get_own_sources(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that fetching the sources for a provider returns only their sources."""
    session, objs = standard_database

    response = await http_client['get']('/api/sources',
                                        token=auth_token(objs['users']['provider']))
    assert response.code == 200
    sources = json.load(response.buffer)['data']
    assert len(sources) == 1


@pytest.mark.asyncio
async def test_admin_get_sources(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the admin gets all sources."""
    session, objs = standard_database

    response = await http_client['get']('/api/sources',
                                        token=auth_token(objs['users']['admin']))
    assert response.code == 200
    sources = json.load(response.buffer)['data']
    assert len(sources) == 2


@pytest.mark.asyncio
async def test_get_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that the fetching a single source works."""
    session, objs = standard_database

    response = await http_client['get'](f'/api/sources/{objs["sources"]["source1"]["_id"]}',
                                        token=auth_token(objs['users']['user1']))
    assert response.code == 200
    source = json.load(response.buffer)['data']
    assert source['type'] == 'sources'
    assert source['id'] == objs["sources"]["source1"]["_id"]
    assert 'type' in source['attributes']
    assert 'title' in source['attributes']
    assert 'subtitle' in source['attributes']
    assert 'date' in source['attributes']
    assert 'publisher' in source['attributes']
    assert 'location' in source['attributes']
    assert 'page_numbers' in source['attributes']
    assert 'data' in source['attributes']
    assert Image.open(BytesIO(b64decode(source['attributes']['data'][source['attributes']['data'].find(',') + 1:])))


@pytest.mark.asyncio
async def test_fail_unauthenticated(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that individual sources are only accessible for logged-in users."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['get'](f'/api/sources/{objs["sources"]["source1"]["_id"]}')
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_missing(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting missing sources fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['get']('/api/sources/does-not-exist',
                                 token=auth_token(objs['users']['user1']))
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
