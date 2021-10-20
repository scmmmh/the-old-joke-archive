"""Fixtures for the API tests."""
import json
import pytest

from aiocouch import CouchDB, exception
from secrets import token_hex
from tornado.httpclient import AsyncHTTPClient, HTTPResponse
from typing import Union
from uuid import uuid1


@pytest.fixture
async def empty_database() -> None:
    """Provide an empty database."""
    async with CouchDB('http://localhost:5984', 'main', 'aiZiojoh7Eux') as session:
        try:
            await session.create('_users')
            await session.create('_replicator')
        except exception.PreconditionFailedError:
            pass
        try:
            await session.create('users')
        except exception.PreconditionFailedError:
            db = await session['users']
            await db.delete()
            await session.create('users')
        yield session
        db = await session['users']
        await db.delete()


@pytest.fixture
async def minimal_database(empty_database: CouchDB) -> None:
    """Provide a database with a minimal set of data."""
    users = await empty_database['users']
    admin = await users.create(str(uuid1()))
    admin['email'] = 'admin@example.com'
    admin['name'] = 'The Admin'
    admin['groups'] = ['admin']
    admin['token'] = token_hex(128)
    await admin.save()
    yield empty_database, {'admin': admin}


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

    async def post(url: str, body: Union[str, dict], token: str = None) -> HTTPResponse:
        return await fetch('POST', url, body=body, token=token)

    return {
        'post': post
    }
