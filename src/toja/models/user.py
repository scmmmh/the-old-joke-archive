from datetime import datetime
from sqlalchemy import (Column, Index, Integer, Unicode, DateTime)
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode(191))
    salt = Column(Unicode(255))
    password = Column(Unicode(255))
    trust = Column(Unicode(255))
    status = Column(Unicode(255))
    groups = Column(NestedMutableJson)
    permissions = Column(NestedMutableJson)
    attributes = Column(NestedMutableJson)
    created = Column(DateTime, default=datetime.now)

    def allow(self, user, action):
        """Check whether the given user is allowed to undertake the given action.

        :param user: The user to check for
        :type user: :class:`~toja.models.user.User`
        :param action: The action to check (view, edit, delete)
        :type action: ``str``
        """
        if action == 'view':
            return True
        elif action == 'edit':
            return user.id == self.id
        elif action == 'delete':
            return user.id == self.id
        else:
            return False


Index('users_email_ix', User.email, unique=True, mysql_length=191)
