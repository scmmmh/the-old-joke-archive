"""User models."""
import logging

from aiocouch import CouchDB
from secrets import token_hex
from urllib.parse import urlencode
from typing import List

from .base import Base
from ..utils import config, send_email
from ..validation import TojaValidator, ValidationError


logger = logging.getLogger(name=__name__)


class User(Base):
    """The database class for users."""

    name = 'users'

    create_schema = {
        'type': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['users']
        },
        'attributes': {
            'type': 'dict',
            'schema': {
                'email': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'check_with': 'validate_email',
                    'coerce': 'email',
                },
                'name': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                }
            }
        }
    }

    login_schema = {
        'type': {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': ['users']
        },
        'attributes': {
            'type': 'dict',
            'schema': {
                'email': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'check_with': 'validate_email',
                    'coerce': 'email',
                },
                'token': {
                    'type': 'string',
                    'empty': False,
                }
            }
        }
    }

    @classmethod
    def validate_login(cls: 'Base', obj: dict) -> dict:
        """Validate the ``obj`` as input for logging in."""
        validator = TojaValidator(cls.login_schema)
        if not validator.validate(obj):
            raise ValidationError(validator.errors)
        return validator.document

    def as_jsonapi(self: 'User') -> dict:
        """Return the user object in JSONAPI representation."""
        obj = super().as_jsonapi()
        if 'attributes' in obj:
            if 'token' in obj['attributes']:
                del obj['attributes']['token']
        return obj

    async def check_unique(self: 'User', db: CouchDB) -> None:
        """Check that this user is unique.

        Checks that the only user with the same e-mail address has the same _id.
        """
        async for user in db.find({'email': self._attributes['email']}):
            if user['_id'] != self._id:
                raise ValidationError({'attributes.email': 'This e-mail address is already registered'})

    async def pre_create(self: 'User', db: CouchDB) -> None:
        """Add the necessary groups when creating."""
        self._attributes['groups'] = []
        self._attributes['token'] = token_hex(128)
        if (await db.info())['doc_count'] == 0:
            self._attributes['groups'] = ['admin']

    async def post_create(self: 'User', db: CouchDB) -> None:
        """After creating, automatically send a login e-mail."""
        await self.send_login_email()

    async def send_login_email(self: 'User') -> None:
        """Send the login email."""
        send_email(self._attributes['email'], 'Log in to The Old Joke Archive', f'''Hello {self._attributes["name"]},

Please use the following link to log into The Old Joke Archive:

{config()['server']['base']}/app/user/log-in?{urlencode((('email', self._attributes["email"]), ('token', self._attributes["token"])))}

The Old Joke Automaton.
''')  # noqa: E501

    def allow_access(self: 'Base', action: str, user_id: str, groups: List[str]) -> bool:
        """Check that access is allowed for the given ``action``."""
        if action == 'read':
            if user_id and (self._id == user_id or 'admin' in groups or 'admin:users' in groups):
                return True
        elif action == 'create':
            return True
        elif action == 'update':
            if user_id and (self._id == user_id or 'admin' in groups or 'admin:users' in groups):
                return True
        elif action == 'delete':
            if user_id and (self._id == user_id or 'admin' in groups or 'admin:users' in groups):
                return True
        return False
