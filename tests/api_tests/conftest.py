"""Fixtures for the API tests."""
import aiohttp
import json
import pytest

from aiocouch import CouchDB
from itertools import chain
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from typing import Union


async def create_objects(names: list[str], dbsession: CouchDB) -> dict:
    """Create the objects in the backend with the given names."""
    async with aiohttp.ClientSession() as http_session:
        query = '&'.join([f'obj={name}' for name in names])
        async with http_session.put(f'http://localhost:6543/test?{query}') as response:
            objs = await response.json()
            # data = (await response.content.read()).decode('utf-8')
            # print(data)
            # objs = json.loads(data)
            for dbname, items in objs.items():
                db = await dbsession[dbname]
                for obj_name, obj_id in list(items.items()):
                    items[obj_name] = await db[obj_id]
    return objs


def merge_objects(a: dict, b: dict) -> dict:
    """Merge the two test objects together."""
    result = {}
    for obj_key, obj_value in chain(a.items(), b.items()):
        if obj_key not in result:
            result[obj_key] = {}
        for item_key, item_value in obj_value.items():
            result[obj_key][item_key] = item_value
    return result


@pytest.fixture
async def empty_database() -> None:
    """Provide an empty database."""
    async with aiohttp.ClientSession() as http_session:
        async with http_session.delete('http://localhost:6543/test'):
            pass
        async with http_session.post('http://localhost:6543/test'):
            pass
    async with CouchDB('http://localhost:5984', 'main', 'aiZiojoh7Eux') as session:
        yield session


@pytest.fixture
async def minimal_database(empty_database: CouchDB) -> None:
    """Provide a database with a minimal set of data."""
    objs = await create_objects(['users/admin'], empty_database)
    yield empty_database, objs


@pytest.fixture
async def standard_database(minimal_database: CouchDB) -> None:
    """Provide a database with a standard set of data."""
    session, objs = minimal_database
    objs = merge_objects(objs, await create_objects(['users/one',
                                                     'users/two',
                                                     'users/three',
                                                     'users/four',
                                                     'users/five',
                                                     'users/six',
                                                     'users/seven',
                                                     'users/eight',
                                                     'users/new',
                                                     'users/inactive',
                                                     'users/blocked',
                                                     'users/provider',
                                                     'users/editor',
                                                     'sources/one',
                                                     'sources/two',
                                                     'jokes/one',
                                                     'jokes/two',
                                                     'jokes/three',
                                                     'jokes/four',
                                                     'jokes/five',
                                                     'jokes/six',
                                                     ],
                                                    session))
    yield session, objs


@pytest.fixture
async def http_client() -> None:
    """Provide a HTTP client."""
    client = AsyncHTTPClient()

    response = await client.fetch('http://localhost:6543/app')
    cookie = response.headers['Set-Cookie']
    xsrf_cookie = cookie[cookie.find('_xsrf=') + 6:]
    xsrf_cookie = xsrf_cookie[:xsrf_cookie.find(';')]

    async def fetch(method: str, url: str, body: Union[str, dict] = None, token: str = None) -> HTTPResponse:
        params = {
            'method': method,
            'headers': {
                'Content-Type': 'application/json',
                'X-XSRFToken': xsrf_cookie,
                'Cookie': cookie,
            }
        }
        if body is not None:
            if isinstance(body, str):
                params['body'] = body
            else:
                params['body'] = json.dumps({'data': body})
        if token is not None:
            params['headers']['X-Toja-Auth'] = token
        return await client.fetch(f'http://localhost:6543{url}', **params)

    async def delete(url: str, token: str = None) -> HTTPResponse:
        return await fetch('DELETE', url, token=token)

    async def post(url: str, body: Union[str, dict], token: str = None) -> HTTPResponse:
        return await fetch('POST', url, body=body, token=token)

    async def put(url: str, body: Union[str, dict], token: str = None) -> HTTPResponse:
        return await fetch('PUT', url, body=body, token=token)

    async def get(url: str, token: str = None) -> HTTPResponse:
        return await fetch('GET', url, token=token)

    return {
        'delete': delete,
        'get': get,
        'post': post,
        'put': put,
    }
