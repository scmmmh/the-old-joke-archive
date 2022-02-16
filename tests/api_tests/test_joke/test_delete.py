"""Tests for joke creation."""
import pytest

from aiocouch import CouchDB, exception as aio_exc
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_delete_joke_by_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a joke works for an editor."""
    session, objs = standard_database
    response = await http_client['delete'](f'/api/jokes/{objs["jokes"]["joke1"]["_id"]}',
                                           token=auth_token(objs['users']['editor']))
    assert response.code == 204
    jokes_db = await session['jokes']
    with pytest.raises(aio_exc.NotFoundError):
        await jokes_db[objs['jokes']['joke1']['_id']]


@pytest.mark.asyncio
async def test_delete_extracted_joke(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting a joke works for the user who extracted it."""
    session, objs = standard_database
    response = await http_client['delete'](f'/api/jokes/{objs["jokes"]["joke2"]["_id"]}',
                                           token=auth_token(objs['users']['user1']))
    assert response.code == 204
    jokes_db = await session['jokes']
    with pytest.raises(aio_exc.NotFoundError):
        await jokes_db[objs['jokes']['joke2']['_id']]


@pytest.mark.asyncio
async def test_fail_delete_extraction_verified_joke(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that deleting fails if the joke has been verified."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['delete'](f'/api/jokes/{objs["jokes"]["joke3"]["_id"]}',
                                    token=auth_token(objs['users']['user1']))
        assert exc_info.value.code == 403
    jokes_db = await session['jokes']
    joke = await jokes_db[objs['jokes']['joke3']['_id']]
    assert joke is not None
