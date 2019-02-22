from datetime import datetime
from sqlalchemy import (Column, Index, Integer, Unicode, ForeignKey, DateTime)
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class Image(Base):

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('images.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    attributes = Column(NestedMutableJson)
    type = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=None, onupdate=datetime.now)


Index('images_parent_ix', Image.parent_id)
Index('images_owner_ix', Image.owner_id)
