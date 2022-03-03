"""Handler for test setup requests."""
import json
import logging

from aiocouch import CouchDB, Document
from aiocouch.attachment import Attachment
from datetime import datetime, timedelta
from importlib import resources, import_module
from io import BytesIO
from jinja2 import Environment
from PIL import Image
from tornado.web import RequestHandler
from uuid import uuid1

from toja.setup import setup_backend, reset_backend
from toja.utils import couchdb
from .. import test


logger = logging.getLogger(__name__)


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


async def create_joke1(objs: dict) -> None:
    """Create the test auto-transcribed joke user."""
    async with couchdb() as dbsession:
        await create_object('users', 'one', objs)
        await create_object('sources', 'one', objs)
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
                    'user': objs['users']['one'],
                    'created': datetime.utcnow().timestamp(),
                },
                'extraction-verified': None,
                'transcribed': [],
                'transcription-verified': None,
                'category-verified': None,
                'annotated': None,
                'annotation-verified': None,
            },
            'source_id': objs['sources']['one'],
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
        await create_object('users', 'one', objs)
        await create_object('sources', 'one', objs)
        joke = await create_singleton_object(dbsession, 'jokes', {
            'test_name_': 'joke2',
            'title': '[Untitled]',
            'status': 'extracted',
            'coordinates': [20, 20, 200, 60],
            'transcriptions': {},
            'activity': {
                'extracted': {
                    'user': objs['users']['one'],
                    'created': datetime.utcnow().timestamp(),
                },
                'extraction-verified': None,
                'transcribed': [],
                'transcription-verified': None,
                'category-verified': None,
                'annotated': None,
                'annotation-verified': None,
            },
            'source_id': objs['sources']['one'],
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
        await create_object('users', 'one', objs)
        await create_object('sources', 'one', objs)
        joke = await create_singleton_object(dbsession, 'jokes', {
            'test_name_': 'joke3',
            'title': '[Untitled]',
            'status': 'extraction-verified',
            'coordinates': [20, 20, 200, 60],
            'transcriptions': {},
            'activity': {
                'extracted': {
                    'user': objs['users']['one'],
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
            'source_id': objs['sources']['one'],
        })
        image = Attachment(joke, 'image')
        img = Image.open(BytesIO(resources.open_binary(test, "example-joke1.png").read()))
        buffer = BytesIO()
        img.save(buffer, format='png')
        await image.save(buffer.getvalue(), 'image/png')
        objs['jokes']['joke3'] = joke['_id']


async def create_object(obj_type: str, obj_name: str, objs: dict) -> Document:
    """Create a new database object."""
    async def get_db_id(path: str) -> str:
        """Get the database id of the given object path."""
        obj = await create_object(*path.split('/'), objs)
        return obj['_id']

    def timestamp(dt: datetime) -> float:
        """Return a datetime's timestamp."""
        return dt.timestamp()

    def timedelta_add(dt: datetime, days: int) -> datetime:
        """Add a timedelta to a datetime."""
        return dt + timedelta(days=days)

    def timedelta_subtract(dt: datetime, days: int) -> datetime:
        """Subtract a timedelta to a datetime."""
        return dt - timedelta(days=days)

    logger.debug(f'Creating object {obj_type}/{obj_name}')
    async with couchdb() as dbsession:
        db = await dbsession[obj_type]
        async for db_obj in db.find({'test_name_': f'{obj_type}/{obj_name}'}):
            logger.debug('Reusing existing database instance')
            if obj_name not in objs[obj_type]:
                objs[obj_type][obj_name] = db_obj['_id']
            return db_obj
        mdl = import_module(f'toja.server.handlers.test.fixtures.{obj_type}')
        obj_data = resources.open_text(mdl, f'{obj_name}.json')
        env = Environment(enable_async=True)
        env.filters['db_id'] = get_db_id
        env.filters['timestamp'] = timestamp
        env.filters['timedelta_add'] = timedelta_add
        env.filters['timedelta_subtract'] = timedelta_subtract
        env.globals['utcnow'] = datetime.utcnow()
        tmpl = env.from_string(obj_data.read())
        obj = json.loads(await tmpl.render_async())
        db_obj = await db.create(str(uuid1()))
        db_obj['test_name_'] = f'{obj_type}/{obj_name}'
        for key, value in obj.items():
            if not key.startswith('_'):
                db_obj[key] = value
        await db_obj.save()
        if '_attachment' in obj:
            image = Attachment(db_obj, obj['_attachment']['name'])
            await image.save(resources.open_binary(mdl, obj['_attachment']['filename']).read(),
                             obj['_attachment']['mimetype'])
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
            if key == 'joke1':
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
