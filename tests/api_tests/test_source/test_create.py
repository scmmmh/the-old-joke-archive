"""Tests for source creation."""
import json
import pytest

from aiocouch import CouchDB
from base64 import b64encode
from importlib import resources
from tornado.httpclient import HTTPClientError
from typing import Tuple

from .. import test_source
from ..util import auth_token


@pytest.mark.asyncio
async def test_create_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source from a png image works."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(test_source, "example-source1.png").read()).decode("utf-8")}'  # noqa: E501
    response = await http_client['post']('/api/sources',
                                         body={'type': 'sources',
                                               'attributes': {'type': 'book',
                                                              'title': 'The Big Book of Bad Jokes',
                                                              'subtitle': 'Nothing as bad as a bad laugh',
                                                              'date': '1860-06',
                                                              'location': 'London, UK',
                                                              'publisher': 'Groan Publishing',
                                                              'page_numbers': '75',
                                                              'data': image_data}},
                                         token=auth_token(objs['users']['provider']))
    assert response.code == 201
    source = json.load(response.buffer)['data']
    assert source
    assert source['attributes']['type'] == 'book'
    assert source['attributes']['title'] == 'The Big Book of Bad Jokes'
    assert source['attributes']['subtitle'] == 'Nothing as bad as a bad laugh'
    assert source['attributes']['date'] == '1860-06'
    assert source['attributes']['location'] == 'London, UK'
    assert source['attributes']['publisher'] == 'Groan Publishing'
    assert source['attributes']['page_numbers'] == '75'
    assert source['attributes']['data'].startswith('data:image/png;base64,')


@pytest.mark.asyncio
async def test_create_minimal_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with minimal metadata works."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(test_source, "example-source1.png").read()).decode("utf-8")}'  # noqa: E501
    response = await http_client['post']('/api/sources',
                                         body={'type': 'sources',
                                               'attributes': {'type': 'book',
                                                              'title': 'The Big Book of Bad Jokes',
                                                              'subtitle': '',
                                                              'date': '1860',
                                                              'location': '',
                                                              'publisher': '',
                                                              'page_numbers': '',
                                                              'data': image_data}},
                                         token=auth_token(objs['users']['provider']))
    assert response.code == 201
    source = json.load(response.buffer)['data']
    assert source
    assert source['attributes']['type'] == 'book'
    assert source['attributes']['title'] == 'The Big Book of Bad Jokes'
    assert source['attributes']['subtitle'] == ''
    assert source['attributes']['date'] == '1860'
    assert source['attributes']['location'] == ''
    assert source['attributes']['publisher'] == ''
    assert source['attributes']['page_numbers'] == ''
    assert source['attributes']['data'].startswith('data:image/png;base64,')


@pytest.mark.asyncio
async def test_create_jpeg_source(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with JPEG image data works."""
    session, objs = standard_database

    image_data = f'data:image/jpeg;base64,{b64encode(resources.open_binary(test_source, "example-source2.jpeg").read()).decode("utf-8")}'  # noqa: E501
    response = await http_client['post']('/api/sources',
                                         body={'type': 'sources',
                                               'attributes': {'type': 'newspaper',
                                                              'title': 'The Daily Joke',
                                                              'subtitle': '',
                                                              'date': '1872-04-13',
                                                              'location': '',
                                                              'publisher': '',
                                                              'page_numbers': '',
                                                              'data': image_data}},
                                         token=auth_token(objs['users']['provider']))
    assert response.code == 201
    source = json.load(response.buffer)['data']
    assert source
    assert source['attributes']['type'] == 'newspaper'
    assert source['attributes']['title'] == 'The Daily Joke'
    assert source['attributes']['subtitle'] == ''
    assert source['attributes']['date'] == '1872-04-13'
    assert source['attributes']['location'] == ''
    assert source['attributes']['publisher'] == ''
    assert source['attributes']['page_numbers'] == ''
    assert source['attributes']['data'].startswith('data:image/png;base64,')


@pytest.mark.asyncio
async def test_create_fail_invalid_type(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with an invalid type fails."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(test_source, "example-source1.png").read()).decode("utf-8")}'  # noqa: E501
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/sources',
                                  body={'type': 'sources',
                                        'attributes': {'type': 'letter',
                                                       'title': 'A letter I just wrote',
                                                       'subtitle': '',
                                                       'date': '1888',
                                                       'location': '',
                                                       'publisher': '',
                                                       'page_numbers': '',
                                                       'data': image_data}},
                                  token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_create_fail_no_title(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with no title fails."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(test_source, "example-source1.png").read()).decode("utf-8")}'  # noqa: E501
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/sources',
                                  body={'type': 'sources',
                                        'attributes': {'type': 'book',
                                                       'title': '',
                                                       'subtitle': '',
                                                       'date': '1888',
                                                       'location': '',
                                                       'publisher': '',
                                                       'page_numbers': '',
                                                       'data': image_data}},
                                  token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_create_fail_no_date(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with no date fails."""
    session, objs = standard_database

    image_data = f'data:image/png;base64,{b64encode(resources.open_binary(test_source, "example-source1.png").read()).decode("utf-8")}'  # noqa: E501
    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/sources',
                                  body={'type': 'sources',
                                        'attributes': {'type': 'book',
                                                       'title': 'An unknown book',
                                                       'subtitle': '',
                                                       'date': '',
                                                       'location': '',
                                                       'publisher': '',
                                                       'page_numbers': '',
                                                       'data': image_data}},
                                  token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_create_fail_no_data(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with no image data fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/sources',
                                  body={'type': 'sources',
                                        'attributes': {'type': 'book',
                                                       'title': 'An idea for a book',
                                                       'subtitle': '',
                                                       'date': '1922',
                                                       'location': '',
                                                       'publisher': '',
                                                       'page_numbers': '',
                                                       'data': ''}},
                                  token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data


@pytest.mark.asyncio
async def test_create_fail_invalid_data(standard_database: Tuple[CouchDB, dict], http_client: dict) -> None:
    """Test that creating a source with invalid data fails."""
    session, objs = standard_database

    with pytest.raises(HTTPClientError) as exc_info:
        await http_client['post']('/api/sources',
                                  body={'type': 'sources',
                                        'attributes': {'type': 'book',
                                                       'title': 'Pure Text',
                                                       'subtitle': '',
                                                       'date': '2021',
                                                       'location': '',
                                                       'publisher': '',
                                                       'page_numbers': '',
                                                       'data': 'data:image/png;base64,fh832hjkfdhn3rh8923nenfe'}},
                                  token=auth_token(objs['users']['provider']))
    assert exc_info.value.code == 400
    data = json.load(exc_info.value.response.buffer)
    assert 'errors' in data
