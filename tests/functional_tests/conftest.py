"""Fixtures for the API tests."""
import bcrypt
import pytest
import yaml

from aiocouch import CouchDB, exception
from datetime import datetime, timedelta
from secrets import token_hex
from uuid import uuid1

from toja.cli import validate_config
from toja.utils import set_config


ADMIN_PWD = bcrypt.hashpw(b'admin1pwd', bcrypt.gensalt()).decode('utf-8')
USER1_PWD = bcrypt.hashpw(b'user1pwd', bcrypt.gensalt()).decode('utf-8')


@pytest.fixture
async def config() -> None:
    """Load and set the configuration."""
    with open('config.yml') as in_f:
        config = yaml.load(in_f, Loader=yaml.FullLoader)
    normalised = validate_config(config)
    set_config(normalised)


@pytest.fixture
async def empty_database(config: None) -> None:
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
    admin['tokens'] = [{'token': token_hex(128),
                        'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
    admin['password'] = ADMIN_PWD
    admin['status'] = 'active'
    admin['last_access'] = datetime.utcnow().timestamp()
    await admin.save()
    yield empty_database, {'admin': admin}


@pytest.fixture
async def standard_database(minimal_database: CouchDB) -> None:
    """Provide a database with a standard set of data."""
    session, objs = minimal_database
    users = await session['users']
    user1 = await users.create(str(uuid1()))
    user1['email'] = 'user1@example.com'
    user1['name'] = 'User One'
    user1['groups'] = []
    user1['tokens'] = [{'token': token_hex(128),
                        'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
    user1['password'] = USER1_PWD
    user1['status'] = 'active'
    user1['last_access'] = datetime.utcnow().timestamp()
    await user1.save()
    objs['user1'] = user1
    yield session, objs
