from datetime import datetime
from sqlalchemy import (Column, Index, Integer, Unicode, DateTime)
from sqlalchemy_json import MutableJson, NestedMutableJson

from .meta import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(Unicode(191))
    salt = Column(Unicode(255))
    password = Column(Unicode(255))
    name = Column(Unicode(255))
    trust = Column(Unicode(255))
    status = Column(Unicode(255))
    groups = Column(NestedMutableJson)
    permissions = Column(NestedMutableJson)
    attributes = Column(NestedMutableJson)
    created = Column(DateTime, default=datetime.now)


Index('users_email_ix', User.email, unique=True, mysql_length=191)
