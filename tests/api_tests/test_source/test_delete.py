"""Tests for source creation."""
import json
import pytest

from aiocouch import CouchDB, exception as aio_exc
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_delete_own_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that delete the source works."""
    session, objs = standard_database

    response = await http_client['delete'](f'/api/sources/{objs["sources"]["source2"]["_id"]}',
                                           token=auth_token(objs['users']['provider']))
    assert response.code == 204
    sources_db = await session['sources']
    with pytest.raises(aio_exc.NotFoundError):
        await sources_db[objs['sources']['source2']['_id']]


@pytest.mark.asyncio
async def test_admin_delete_any_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that delete the source works."""
    session, objs = standard_database

    response = await http_client['delete'](f'/api/sources/{objs["sources"]["source2"]["_id"]}',
                                           token=auth_token(objs['users']['admin']))
    assert response.code == 204
    sources_db = await session['sources']
    with pytest.raises(aio_exc.NotFoundError):
        await sources_db[objs['sources']['source2']['_id']]


@pytest.mark.asyncio
async def test_fail_delete_missing(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a non-existent source fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete']('/api/sources/does-not-exist',
                                    token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_delete_other_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a source of another user fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete'](f'/api/sources/{objs["sources"]["source1"]["_id"]}',
                                    token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
