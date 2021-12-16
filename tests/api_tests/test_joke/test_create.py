"""Tests for joke creation."""
import json
import pytest

from aiocouch import CouchDB
from aiocouch.attachment import Attachment
from io import BytesIO
from PIL import Image
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token


@pytest.mark.asyncio
async def test_create_joke_by_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a joke from a source works for an editor."""
    session, objs = standard_database
    response = await http_client['post']('/api/jokes',
                                         body={'type': 'jokes',
                                               'attributes': {'coordinates': [25, 13, 213, 55]},
                                               'relationships': {'source': {'data': {'type': 'sources',
                                                                                     'id': objs['sources']['source1']['_id']}}}},  # noqa: E501
                                         token=auth_token(objs['users']['editor']))
    assert response.code == 201
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['status'] == 'extraction-verified'
    assert joke['attributes']['coordinates'] == [25, 13, 213, 55]
    assert joke['attributes']['activity']['extracted']['user'] == objs['users']['editor']['_id']
    assert joke['attributes']['activity']['extraction-verified']['user'] == objs['users']['editor']['_id']
    jokes_db = await session['jokes']
    db_joke = await jokes_db[joke['id']]
    image = Attachment(db_joke, 'image')
    with Image.open(BytesIO(await image.fetch())) as img:
        assert img
        assert img.size == (188, 42)


@pytest.mark.asyncio
async def test_create_joke_user1(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a joke from a source works for a normal user."""
    session, objs = standard_database
    response = await http_client['post']('/api/jokes',
                                         body={'type': 'jokes',
                                               'attributes': {'coordinates': [25, 13, 213, 55]},
                                               'relationships': {'source': {'data': {'type': 'sources',
                                                                                     'id': objs['sources']['source1']['_id']}}}},  # noqa: E501
                                         token=auth_token(objs['users']['user1']))
    assert response.code == 201
    joke = json.load(response.buffer)['data']
    assert joke
    assert joke['attributes']['title'] == '[Untitled]'
    assert joke['attributes']['status'] == 'extracted'
    assert joke['attributes']['coordinates'] == [25, 13, 213, 55]
    assert joke['attributes']['activity']['extracted']['user'] == objs['users']['user1']['_id']
    jokes_db = await session['jokes']
    db_joke = await jokes_db[joke['id']]
    image = Attachment(db_joke, 'image')
    with Image.open(BytesIO(await image.fetch())) as img:
        assert img
        assert img.size == (188, 42)


@pytest.mark.asyncio
async def test_fail_create_joke_non_logged_in(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a joke without a logged-in user fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/jokes',
                                  body={'type': 'jokes',
                                        'attributes': {'coordinates': [25, 13, 213, 55]},
                                        'relationships': {'source': {'data': {'type': 'sources',
                                                                              'id': objs['sources']['source1']['_id']}}}})  # noqa: E501
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_create_joke_from_non_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a joke from a non-existent source fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/jokes',
                                  body={'type': 'jokes',
                                        'attributes': {'coordinates': [25, 13, 213, 55]},
                                        'relationships': {'source': {'data': {'type': 'sources',
                                                                              'id': 'does-not-exist'}}}},
                                  token=auth_token(objs['users']['editor']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_create_joke_no_coordinates(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a joke without coordinates fails."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/jokes',
                                  body={'type': 'jokes',
                                        'attributes': {},
                                        'relationships': {'source': {'data': {'type': 'sources',
                                                                              'id': objs['sources']['source1']['_id']}}}},  # noqa: E501
                                  token=auth_token(objs['users']['editor']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
