"""Handler for test setup requests."""
import json
import logging

from aiocouch import Document
from aiocouch.attachment import Attachment
from datetime import datetime, timedelta
from importlib import resources, import_module
from jinja2 import Environment
from tornado.web import RequestHandler
from uuid import uuid1

from toja.setup import setup_backend, reset_backend
from toja.utils import couchdb


logger = logging.getLogger(__name__)


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
            await create_object(*key.split('/'), objs)
        self.write(objs)

    async def delete(self: 'TestHandler') -> None:
        """Delete the backend setup."""
        await reset_backend()

    def check_xsrf_cookie(self: 'TestHandler') -> None:
        """No XSRF cookie support needed."""
        return False
