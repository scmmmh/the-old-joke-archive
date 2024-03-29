"""Tests for joke access."""
import json
import pytest

from aiocouch import CouchDB
from tornado.httpclient import HTTPClientError
from typing import Tuple

from ..util import auth_token, async_gen_to_list


@pytest.mark.asyncio
async def test_get_all_jokes_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting all jokes works for an admin."""
    session, objs = standard_database
    response = await http_client['get']('/api/jokes',
                                        token=auth_token(objs['users']['admin']))
    assert response.code == 200
    jokes = json.load(response.buffer)['data']
    jokes_db = await session['jokes']
    db_jokes = await async_gen_to_list(jokes_db.docs())
    assert len(jokes) == len(db_jokes)
    for joke in jokes:
        assert 'attributes' in joke
        assert 'title' in joke['attributes']
        assert 'data' in joke['attributes']
        assert 'transcriptions' in joke['attributes']
        assert 'status' in joke['attributes']
        assert 'activity' in joke['attributes']
        assert 'relationships' in joke
        assert 'source' in joke['relationships']


@pytest.mark.asyncio
async def test_get_all_jokes_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting all jokes works for an editor."""
    session, objs = standard_database
    response = await http_client['get']('/api/jokes',
                                        token=auth_token(objs['users']['editor']))
    assert response.code == 200
    jokes = json.load(response.buffer)['data']
    jokes_db = await session['jokes']
    db_jokes = await async_gen_to_list(jokes_db.docs())
    assert len(jokes) == len(db_jokes)
    for joke in jokes:
        assert 'attributes' in joke
        assert 'title' in joke['attributes']
        assert 'data' in joke['attributes']
        assert 'transcriptions' in joke['attributes']
        assert 'status' in joke['attributes']
        assert 'activity' in joke['attributes']
        assert 'relationships' in joke
        assert 'source' in joke['relationships']


@pytest.mark.asyncio
async def test_get_all_jokes_general_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting all jokes works for a logged-in user."""
    session, objs = standard_database
    response = await http_client['get']('/api/jokes',
                                        token=auth_token(objs['users']['one']))
    assert response.code == 200
    jokes = json.load(response.buffer)['data']
    jokes_db = await session['jokes']
    db_jokes = await async_gen_to_list(jokes_db.docs())
    assert len(jokes) == len(db_jokes)
    for joke in jokes:
        assert 'attributes' in joke
        assert 'title' in joke['attributes']
        assert 'data' in joke['attributes']
        assert 'transcriptions' in joke['attributes']
        assert 'status' in joke['attributes']
        assert 'activity' in joke['attributes']
        assert 'relationships' in joke
        assert 'source' in joke['relationships']


@pytest.mark.asyncio
async def test_fail_get_all_jokes_non_logged_in(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting all jokes fails if the user is logged out."""
    session, objs = standard_database
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['get']('/api/jokes')
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_get_joke_admin(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting a single joke works for an admin."""
    session, objs = standard_database
    response = await http_client['get'](f'/api/jokes/{objs["jokes"]["one"]["_id"]}',
                                        token=auth_token(objs['users']['admin']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert 'attributes' in joke
    assert 'title' in joke['attributes']
    assert 'data' in joke['attributes']
    assert 'transcriptions' in joke['attributes']
    assert 'status' in joke['attributes']
    assert 'activity' in joke['attributes']
    assert 'relationships' in joke
    assert 'source' in joke['relationships']


@pytest.mark.asyncio
async def test_get_joke_editor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting a single joke works for an editor."""
    session, objs = standard_database
    response = await http_client['get'](f'/api/jokes/{objs["jokes"]["one"]["_id"]}',
                                        token=auth_token(objs['users']['editor']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert 'attributes' in joke
    assert 'title' in joke['attributes']
    assert 'data' in joke['attributes']
    assert 'transcriptions' in joke['attributes']
    assert 'status' in joke['attributes']
    assert 'activity' in joke['attributes']
    assert 'relationships' in joke
    assert 'source' in joke['relationships']


@pytest.mark.asyncio
async def test_get_joke_contributor(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting a single joke works for a logged-in user."""
    session, objs = standard_database
    response = await http_client['get'](f'/api/jokes/{objs["jokes"]["one"]["_id"]}',
                                        token=auth_token(objs['users']['provider']))
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert 'attributes' in joke
    assert 'title' in joke['attributes']
    assert 'data' in joke['attributes']
    assert 'transcriptions' in joke['attributes']
    assert 'status' in joke['attributes']
    assert 'activity' in joke['attributes']
    assert 'relationships' in joke
    assert 'source' in joke['relationships']


'''
@pytest.mark.asyncio
async def test_get_published_joke_anonymous(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting a published joke works for a logged-in user."""
    session, objs = standard_database
    response = await http_client['get'](f'/api/jokes/{objs["jokes"]["one"]["_id"]}')
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert 'attributes' in joke
    assert 'title' in joke['attributes']
    assert 'data' in joke['attributes']
    assert 'transcriptions' in joke['attributes']
    assert 'status' in joke['attributes']
    assert 'activity' in joke['attributes']
    assert 'relationships' in joke
    assert 'source' in joke['relationships']


@pytest.mark.asyncio
async def test_get_unpublished_joke_anonymous_fail(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that getting a published joke works for a logged-in user."""
    session, objs = standard_database
    response = await http_client['get'](f'/api/jokes/{objs["jokes"]["joke2"]["_id"]}')
    assert response.code == 200
    joke = json.load(response.buffer)['data']
    assert 'attributes' in joke
    assert 'title' in joke['attributes']
    assert 'data' in joke['attributes']
    assert 'transcriptions' in joke['attributes']
    assert 'status' in joke['attributes']
    assert 'activity' in joke['attributes']
    assert 'relationships' in joke
    assert 'source' in joke['relationships']
'''  # noqa
