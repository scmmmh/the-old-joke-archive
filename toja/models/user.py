"""User models."""
from aiocouch import CouchDB

from .base import Base
from ..validation import ValidationError


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
        if (await db.info())['doc_count'] == 0:
            self._attributes['groups'] = ['admin']

    async def post_create(self: 'Base', db: CouchDB) -> None:
        """After creating, automatically send a login e-mail."""
        pass
