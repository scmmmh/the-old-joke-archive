"""Tests for joke editing."""
import json
import pytest

from aiocouch import CouchDB
from aiocouch.attachment import Attachment
from io import BytesIO
from PIL import Image
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_update_extracted_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test confirming that updating the extracted co-ordinates works for an editor."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["two"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['two']['_id'],
                                              'attributes': {'coordinates': [20, 13, 213, 55]},
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['editor']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['status'] == 'extraction-verified'
    assert joke['attributes']['coordinates'] == [20, 13, 213, 55]
    assert joke['attributes']['activity']['extraction-verified']['user'] == objs['users']['editor']['_id']
    jokes_db = await session['jokes']
    db_joke = await jokes_db[joke['id']]
    image = Attachment(db_joke, 'image')
    with Image.open(BytesIO(await image.fetch())) as img:
        assert img
        assert img.size == (322, 41)


@pytest.mark.asyncio
async def test_update_extracted_same_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test confirming that updating the extracted co-ordinates works for an editor."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["two"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['two']['_id'],
                                              'attributes': {'coordinates': [20, 13, 213, 55]},
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['one']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['status'] == 'extracted'
    assert joke['attributes']['coordinates'] == [20, 13, 213, 55]
    assert joke['attributes']['activity']['extracted']['user'] == objs['users']['one']['_id']
    jokes_db = await session['jokes']
    db_joke = await jokes_db[joke['id']]
    image = Attachment(db_joke, 'image')
    with Image.open(BytesIO(await image.fetch())) as img:
        assert img
        assert img.size == (322, 41)


@pytest.mark.asyncio
async def test_confirm_extraction_verified_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test confirming the extraction verification works for an editor."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["two"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['two']['_id'],
                                              'attributes': {'status': 'extraction-verified'},
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['editor']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['status'] == 'extraction-verified'
    assert joke['attributes']['activity']['extraction-verified']['user'] == objs['users']['editor']['_id']


@pytest.mark.asyncio
async def test_confirm_extraction_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test confirming the extraction verification works for a user who did not extract the joke."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["two"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['two']['_id'],
                                              'attributes': {'status': 'extraction-verified'},
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['two']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['status'] == 'extraction-verified'
    assert joke['attributes']['activity']['extraction-verified']['user'] == objs['users']['two']['_id']


@pytest.mark.asyncio
async def test_fail_extraction_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test confirming the extraction fails for a user who did extract the joke."""
    session, objs = standard_database
    response = await http_client['put'](f'/api/jokes/{objs["jokes"]["two"]["_id"]}',
                                        body={'type': 'jokes',
                                              'id': objs['jokes']['two']['_id'],
                                              'attributes': {'status': 'extraction-verified'},
                                              'relationships': {'source': {'data': {'type': 'sources',
                                                                                    'id': objs['sources']['one']['_id']}}}},  # noqa: E501
                                        token=auth_token(objs['users']['one']))
    assert response.code == 200
    jokes_db = await session['jokes']
    joke = await jokes_db[objs['jokes']['two']['_id']]
    assert joke is not None
    assert joke['status'] == 'extracted'
    assert joke['activity']['extraction-verified'] is None
