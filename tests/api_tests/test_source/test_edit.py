"""Tests for source creation."""
import json
import pytest

from aiocouch import CouchDB
from base64 import b64encode
from importlib import resources
from tornado.httpclient import HTTPClientError
from typing import Tuple

from toja.server.handlers.test.fixtures import sources

from ..util import auth_token


@pytest.mark.asyncio
async def test_update_own_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating the source works."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(sources, "one.png").read()).decode("utf-8")}'  # noqa: E501
    response = await http_client['put'](f'/api/sources/{objs["sources"]["two"]["_id"]}',
                                        body={'type': 'sources',
                                              'id': objs['sources']['two']['_id'],
                                              'attributes': {
                                                  'type': 'book',
                                                  'title': 'All change',
                                                  'subtitle': 'New subtitle',
                                                  'date': '2021-04-01',
                                                  'publisher': 'No such press',
                                                  'location': 'Nowhere',
                                                  'page_numbers': '10',
                                                  'data': image_data,
                                              }},
                                        token=auth_token(objs['users']['provider']))
    assert response.code == 200
    source = json.load(response.buffer)['data']
    sources_db = await session['sources']
    db_source = await sources_db[source['id']]
    assert db_source['type'] == 'book'
    assert db_source['title'] == 'All change'
    assert db_source['subtitle'] == 'New subtitle'
    assert db_source['date'] == '2021-04-01'
    assert db_source['publisher'] == 'No such press'
    assert db_source['location'] == 'Nowhere'
    assert db_source['page_numbers'] == '10'
    assert db_source['updated'] > db_source['created']


@pytest.mark.asyncio
async def test_minimal_update_own_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that minimal updating works."""
    session, objs = standard_database

    response = await http_client['put'](f'/api/sources/{objs["sources"]["two"]["_id"]}',
                                        body={'type': 'sources',
                                              'id': objs['sources']['two']['_id'],
                                              'attributes': {
                                              }},
                                        token=auth_token(objs['users']['provider']))
    assert response.code == 200
    source = json.load(response.buffer)['data']
    sources_db = await session['sources']
    db_source = await sources_db[source['id']]
    assert db_source['type'] == 'newspaper'
    assert db_source['title'] == 'The Daily Joke'
    assert db_source['subtitle'] == ''
    assert db_source['date'] == '1872-04-13'
    assert db_source['publisher'] == ''
    assert db_source['location'] == ''
    assert db_source['page_numbers'] == ''
    assert db_source['updated'] > db_source['created']


@pytest.mark.asyncio
async def test_admin_update_other_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating any source by the admin works."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(sources, "one.png").read()).decode("utf-8")}'  # noqa: E501
    response = await http_client['put'](f'/api/sources/{objs["sources"]["two"]["_id"]}',
                                        body={'type': 'sources',
                                              'id': objs['sources']['two']['_id'],
                                              'attributes': {
                                                  'type': 'book',
                                                  'title': 'All change',
                                                  'subtitle': 'New subtitle',
                                                  'date': '2021-04-01',
                                                  'publisher': 'No such press',
                                                  'location': 'Nowhere',
                                                  'page_numbers': '10',
                                                  'data': image_data,
                                              }},
                                        token=auth_token(objs['users']['admin']))
    assert response.code == 200
    source = json.load(response.buffer)['data']
    sources_db = await session['sources']
    db_source = await sources_db[source['id']]
    assert db_source['type'] == 'book'
    assert db_source['title'] == 'All change'
    assert db_source['subtitle'] == 'New subtitle'
    assert db_source['date'] == '2021-04-01'
    assert db_source['publisher'] == 'No such press'
    assert db_source['location'] == 'Nowhere'
    assert db_source['page_numbers'] == '10'
    assert db_source['updated'] > db_source['created']


@pytest.mark.asyncio
async def test_fail_missing(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a non-existant source fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put']('/api/sources/does-not-exist',
                                 body={'type': 'sources',
                                       'id': 'does-not-exist',
                                       'attributes': {
                                           'type': 'book',
                                           'title': 'All change',
                                           'subtitle': 'New subtitle',
                                           'date': '2021-04-01',
                                           'publisher': 'No such press',
                                           'location': 'Nowhere',
                                           'page_numbers': '10',
                                       }},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 404
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_other_user(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating a source belonging to another user fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/sources/{objs["sources"]["one"]["_id"]}',
                                 body={'type': 'sources',
                                       'id': objs['sources']['one']['_id'],
                                       'attributes': {
                                           'type': 'book',
                                           'title': 'All change',
                                           'subtitle': 'New subtitle',
                                           'date': '2021-04-01',
                                           'publisher': 'No such press',
                                           'location': 'Nowhere',
                                           'page_numbers': '10',
                                       }},
                                 token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 403
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_invalid_type(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with an invalid type fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/sources/{objs["sources"]["one"]["_id"]}',
                                 body={'type': 'sources',
                                       'id': objs['sources']['one']['_id'],
                                       'attributes': {
                                           'type': 'letter',
                                       }},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_invalid_title(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with an invalid title fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/sources/{objs["sources"]["one"]["_id"]}',
                                 body={'type': 'sources',
                                       'id': objs['sources']['one']['_id'],
                                       'attributes': {
                                           'title': '',
                                       }},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_fail_invalid_date(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that updating with an invalid date fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['put'](f'/api/sources/{objs["sources"]["one"]["_id"]}',
                                 body={'type': 'sources',
                                       'id': objs['sources']['one']['_id'],
                                       'attributes': {
                                           'date': '',
                                       }},
                                 token=auth_token(objs['users']['admin']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
