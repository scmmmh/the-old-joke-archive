"""Handler for test setup requests."""
import bcrypt

from datetime import datetime, timedelta
from secrets import token_hex
from tornado.web import RequestHandler
from uuid import uuid1

from toja.setup import setup_backend, reset_backend
from toja.utils import couchdb


ADMIN_PWD = bcrypt.hashpw(b'adminpwd', bcrypt.gensalt()).decode('utf-8')
USER1_PWD = bcrypt.hashpw(b'user1pwd', bcrypt.gensalt()).decode('utf-8')
USERBLOCKED_PWD = bcrypt.hashpw(b'userBlockedpwd', bcrypt.gensalt()).decode('utf-8')
USERINACTIVE_PWD = bcrypt.hashpw(b'userInactivepwd', bcrypt.gensalt()).decode('utf-8')


async def create_user_admin(objs: dict) -> None:
    """Create the test admin user."""
    async with couchdb() as dbsession:
        users = await dbsession['users']
        user = await users.create(str(uuid1()))
        user['email'] = 'admin@example.com'
        user['name'] = 'The Admin'
        user['groups'] = ['admin']
        user['tokens'] = [{'token': token_hex(128),
                           'timestamp': (datetime.utcnow() + timedelta(days=30)).timestamp()}]
        user['password'] = ADMIN_PWD
        user['status'] = 'active'
        user['last_access'] = datetime.utcnow().timestamp()
        await user.save()
        objs['users']['admin'] = user['_id']
        return user


async def create_user_user1(objs: dict) -> None:
    """Create the first normal test user."""
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
        return user


async def create_user_new(objs: dict) -> None:
    """Create a test new user."""
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
        return user


async def create_user_blocked(objs: dict) -> None:
    """Create a test blocked user."""
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
        return user


async def create_user_inactive(objs: dict) -> None:
    """Create a test inactive user."""
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
        return user


class TestHandler(RequestHandler):
    """Handler to create and delete the backend storage."""

    async def post(self: 'TestHandler') -> None:
        """Create the backend setup."""
        await setup_backend()

    async def put(self: 'TestHandler') -> None:
        """Create test objects in the couchdb."""
        objs = {'users': {}}
        for key in self.get_arguments('obj'):
            if key == 'admin':
                await create_user_admin(objs)
            elif key == 'user1':
                await create_user_user1(objs)
            elif key == 'userNew':
                await create_user_new(objs)
            elif key == 'userBlocked':
                await create_user_blocked(objs)
            elif key == 'userInactive':
                await create_user_inactive(objs)
        self.write(objs)

    async def delete(self: 'TestHandler') -> None:
        """Delete the backend setup."""
        await reset_backend()

    def check_xsrf_cookie(self: 'TestHandler') -> None:
        """No XSRF cookie support needed."""
        return False
