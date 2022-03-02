"""Handler for test setup requests."""
import bcrypt
import json

from aiocouch import CouchDB, Document
from aiocouch.attachment import Attachment
from datetime import datetime, timedelta
from importlib import resources, import_module
from io import BytesIO
from jinja2 import Environment
from PIL import Image
from secrets import token_hex
from tornado.web import RequestHandler
from uuid import uuid1

from toja.setup import setup_backend, reset_backend
from toja.utils import couchdb
from .. import test


USER1_PWD = bcrypt.hashpw(b'user1pwd', bcrypt.gensalt()).decode('utf-8')
USERBLOCKED_PWD = bcrypt.hashpw(b'userBlockedpwd', bcrypt.gensalt()).decode('utf-8')
USERINACTIVE_PWD = bcrypt.hashpw(b'userInactivepwd', bcrypt.gensalt()).decode('utf-8')
PROVIDER_PWD = bcrypt.hashpw(b'providerpwd', bcrypt.gensalt()).decode('utf-8')
EDITOR_PWD = bcrypt.hashpw(b'editorpwd', bcrypt.gensalt()).decode('utf-8')


async def create_singleton_object(dbsession: CouchDB, dbname: str, obj: dict) -> Document:
    """Create a singleton CouchDB object with the given parameters."""
    db = await dbsession[dbname]
    async for db_obj in db.find({'test_name_': obj['test_name_']}):
        return db_obj
    db_obj = await db.create(str(uuid1()))
    for key, value in obj.items():
        db_obj[key] = value
    await db_obj.save()
    return db_obj


async def create_user_user1(objs: dict) -> None:
    """Create the first normal test user."""
    if 'user1' not in objs['users']:
        async with couchdb() as dbsession:
            users = await dbsession['users']
            user = await users.create(str(uuid1()))
            user['email'] = 'user1@example.com'
            user['name'] = 'User One'
            user['groups'] = []
            user['tokens'] = [{'token': token_hex(128),
                               'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
            user['password'] = USER1_PWD
            user['status'] = 'active'
            user['last_access'] = datetime.utcnow().timestamp()
            await user.save()
            objs['users']['user1'] = user['_id']


async def create_user_new(objs: dict) -> None:
    """Create a test new user."""
    if 'userNew' not in objs['users']:
        async with couchdb() as dbsession:
            users = await dbsession['users']
            user = await users.create(str(uuid1()))
            user['email'] = 'user_new@example.com'
            user['name'] = 'User New'
            user['groups'] = []
            user['tokens'] = [{'token': token_hex(128),
                               'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
            user['password'] = ''
            user['status'] = 'new'
            user['last_access'] = (datetime.utcnow() - timedelta(days=30)).timestamp()
            await user.save()
            objs['users']['userNew'] = user['_id']


async def create_user_blocked(objs: dict) -> None:
    """Create a test blocked user."""
    if 'userBlocked' not in objs['users']:
        async with couchdb() as dbsession:
            users = await dbsession['users']
            user = await users.create(str(uuid1()))
            user['email'] = 'user_blocked@example.com'
            user['name'] = 'User Blocked'
            user['groups'] = []
            user['tokens'] = [{'token': token_hex(128),
                               'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
            user['password'] = USERBLOCKED_PWD
            user['status'] = 'blocked'
            user['last_access'] = datetime.utcnow().timestamp()
            await user.save()
            objs['users']['userBlocked'] = user['_id']


async def create_user_inactive(objs: dict) -> None:
    """Create a test inactive user."""
    if 'userInactive' not in objs['users']:
        async with couchdb() as dbsession:
            users = await dbsession['users']
            user = await users.create(str(uuid1()))
            user['email'] = 'user_inactive@example.com'
            user['name'] = 'User One'
            user['groups'] = []
            user['tokens'] = [{'token': token_hex(128),
                               'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
            user['password'] = USERINACTIVE_PWD
            user['status'] = 'active'
            user['last_access'] = datetime.utcnow().timestamp()
            await user.save()
            objs['users']['userInactive'] = user['_id']


async def create_user_provider(objs: dict) -> None:
    """Create the test provider user."""
    if 'provider' not in objs['users']:
        async with couchdb() as dbsession:
            users = await dbsession['users']
            user = await users.create(str(uuid1()))
            user['email'] = 'provider@example.com'
            user['name'] = 'Data Provider'
            user['groups'] = ['provider']
            user['tokens'] = [{'token': token_hex(128),
                               'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
            user['password'] = PROVIDER_PWD
            user['status'] = 'active'
            user['last_access'] = datetime.utcnow().timestamp()
            await user.save()
            objs['users']['provider'] = user['_id']


async def create_user_editor(objs: dict) -> None:
    """Create the test editor user."""
    async with couchdb() as dbsession:
        user = await create_singleton_object(dbsession, 'users', {
            'test_name_': 'editor',
            'email': 'editor@example.com',
            'name': 'An Editor',
            'groups': ['editor'],
            'tokens': [{'token': token_hex(128),
                        'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}],
            'password': EDITOR_PWD,
            'status': 'active',
            'last_access': datetime.utcnow().timestamp(),
        })
        objs['users']['editor'] = user['_id']


async def create_source1(objs: dict) -> None:
    """Create the first source."""
    if 'source1' not in objs['sources']:
        await create_object('users', 'admin', objs)
        async with couchdb() as dbsession:
            sources = await dbsession['sources']
            source = await sources.create(str(uuid1()))
            source['type'] = 'book'
            source['title'] = 'The Big Book of Bad Jokes'
            source['subtitle'] = 'Nothing as bad as a bad laugh'
            source['date'] = '1860-06'
            source['location'] = 'London, UK'
            source['publisher'] = 'Groan Publishing'
            source['page_numbers'] = '75'
            source['creator'] = objs['users']['admin']
            source['created'] = datetime.utcnow().timestamp()
            await source.save()
            image = Attachment(source, 'image')
            await image.save(resources.open_binary(test, 'example-source1.png').read(), 'image/png')
            objs['sources']['source1'] = source['_id']


async def create_source2(objs: dict) -> None:
    """Create the second source."""
    if 'source2' not in objs['sources']:
        await create_user_provider(objs)
        async with couchdb() as dbsession:
            sources = await dbsession['sources']
            source = await sources.create(str(uuid1()))
            source['type'] = 'newspaper'
            source['title'] = 'The Daily Joke'
            source['subtitle'] = ''
            source['date'] = '1872-04-13'
            source['location'] = ''
            source['publisher'] = ''
            source['page_numbers'] = ''
            source['creator'] = objs['users']['provider']
            source['created'] = datetime.utcnow().timestamp()
            await source.save()
            image = Attachment(source, 'image')
            img = Image.open(BytesIO(resources.open_binary(test, 'example-source2.jpeg').read()))
            buffer = BytesIO()
            img.save(buffer, format='png')
            await image.save(buffer.getvalue(), 'image/png')
            objs['sources']['source2'] = source['_id']


async def create_joke1(objs: dict) -> None:
    """Create the test auto-transcribed joke user."""
    async with couchdb() as dbsession:
        await create_user_user1(objs)
        await create_source1(objs)
        joke = await create_singleton_object(dbsession, 'jokes', {
            'test_name_': 'joke1',
            'title': '[Untitled]',
            'status': 'auto-transcribed',
            'coordinates': [20, 20, 200, 60],
            'transcriptions': {
                'auto': {
                    'content': {
                        'type': 'doc',
                        'content': [
                            {
                                'type': 'paragraph',
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': 'Why should a sallor always be a good pugilist?'
                                    }
                                ]
                            },
                            {
                                'type': 'paragraph',
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': 'Because he is always boxing the compass'
                                    }
                                ]
                            }
                        ]
                    }
                }
            },
            'activity': {
                'extracted': {
                    'user': objs['users']['user1'],
                    'created': datetime.utcnow().timestamp(),
                },
                'extraction-verified': None,
                'transcribed': [],
                'transcription-verified': None,
                'category-verified': None,
                'annotated': None,
                'annotation-verified': None,
            },
            'source_id': objs['sources']['source1'],
        })
        image = Attachment(joke, 'image')
        img = Image.open(BytesIO(resources.open_binary(test, "example-joke1.png").read()))
        buffer = BytesIO()
        img.save(buffer, format='png')
        await image.save(buffer.getvalue(), 'image/png')
        objs['jokes']['joke1'] = joke['_id']


async def create_joke2(objs: dict) -> None:
    """Create the test extracted joke."""
    async with couchdb() as dbsession:
        await create_user_user1(objs)
        await create_source1(objs)
        joke = await create_singleton_object(dbsession, 'jokes', {
            'test_name_': 'joke2',
            'title': '[Untitled]',
            'status': 'extracted',
            'coordinates': [20, 20, 200, 60],
            'transcriptions': {},
            'activity': {
                'extracted': {
                    'user': objs['users']['user1'],
                    'created': datetime.utcnow().timestamp(),
                },
                'extraction-verified': None,
                'transcribed': [],
                'transcription-verified': None,
                'category-verified': None,
                'annotated': None,
                'annotation-verified': None,
            },
            'source_id': objs['sources']['source1'],
        })
        image = Attachment(joke, 'image')
        img = Image.open(BytesIO(resources.open_binary(test, "example-joke1.png").read()))
        buffer = BytesIO()
        img.save(buffer, format='png')
        await image.save(buffer.getvalue(), 'image/png')
        objs['jokes']['joke2'] = joke['_id']


async def create_joke3(objs: dict) -> None:
    """Create the test extracted joke."""
    async with couchdb() as dbsession:
        await create_user_user1(objs)
        await create_source1(objs)
        joke = await create_singleton_object(dbsession, 'jokes', {
            'test_name_': 'joke3',
            'title': '[Untitled]',
            'status': 'extraction-verified',
            'coordinates': [20, 20, 200, 60],
            'transcriptions': {},
            'activity': {
                'extracted': {
                    'user': objs['users']['user1'],
                    'created': datetime.utcnow().timestamp(),
                },
                'extraction-verified': {
                    'user': objs['users']['editor'],
                    'created': datetime.utcnow().timestamp(),
                },
                'transcribed': [],
                'transcription-verified': None,
                'category-verified': None,
                'annotated': None,
                'annotation-verified': None,
            },
            'source_id': objs['sources']['source1'],
        })
        image = Attachment(joke, 'image')
        img = Image.open(BytesIO(resources.open_binary(test, "example-joke1.png").read()))
        buffer = BytesIO()
        img.save(buffer, format='png')
        await image.save(buffer.getvalue(), 'image/png')
        objs['jokes']['joke3'] = joke['_id']


async def create_object(obj_type: str, obj_name: str, objs: dict) -> Document:
    """Create a new database object."""
    def get_db_id(path: str) -> str:
        """Get the database id of the given object path."""
        return 'hm'

    def timestamp(dt: datetime) -> float:
        """Return a datetime's timestamp."""
        return dt.timestamp()

    def timedelta_add(dt: datetime, days: int) -> datetime:
        """Add a timedelta to a datetime."""
        return dt + timedelta(days=days)

    mdl = import_module(f'toja.server.handlers.test.fixtures.{obj_type}')
    obj_data = resources.open_text(mdl, f'{obj_name}.json')
    env = Environment()
    env.filters['db_id'] = get_db_id
    env.filters['timestamp'] = timestamp
    env.filters['timedelta_add'] = timedelta_add
    env.globals['utcnow'] = datetime.utcnow()
    tmpl = env.from_string(obj_data.read())
    obj = json.loads(tmpl.render())
    obj['test_name_'] = f'{obj_type}/{obj_name}'
    async with couchdb() as dbsession:
        db_obj = await create_singleton_object(dbsession, obj_type, obj)
        objs[obj_type][obj_name] = db_obj['_id']
        return db_obj


class TestHandler(RequestHandler):
    """Handler to create and delete the backend storage."""

    async def post(self: 'TestHandler') -> None:
        """Create the backend setup."""
        await setup_backend()

    async def put(self: 'TestHandler') -> None:
        """Create test objects in the couchdb."""
        objs = {'users': {},
                'sources': {},
                'jokes': {}}
        for key in self.get_arguments('obj'):
            if key == 'user1':
                await create_user_user1(objs)
            elif key == 'userNew':
                await create_user_new(objs)
            elif key == 'userBlocked':
                await create_user_blocked(objs)
            elif key == 'userInactive':
                await create_user_inactive(objs)
            elif key == 'provider':
                await create_user_provider(objs)
            elif key == 'editor':
                await create_user_editor(objs)
            elif key == 'source1':
                await create_source1(objs)
            elif key == 'source2':
                await create_source2(objs)
            elif key == 'joke1':
                await create_joke1(objs)
            elif key == 'joke2':
                await create_joke2(objs)
            elif key == 'joke3':
                await create_joke3(objs)
            elif '/' in key:
                await create_object(*key.split('/'), objs)
        self.write(objs)

    async def delete(self: 'TestHandler') -> None:
        """Delete the backend setup."""
        await reset_backend()

    def check_xsrf_cookie(self: 'TestHandler') -> None:
        """No XSRF cookie support needed."""
        return False
