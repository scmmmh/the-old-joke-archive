from datetime import datetime
from sqlalchemy import (Column, Index, Integer, Unicode, ForeignKey, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class Image(Base):

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('images.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    attributes = Column(NestedMutableJson)
    type = Column(Unicode(255))
    status = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=None, onupdate=datetime.now)

    owner = relationship('User')
    parent = relationship('Image', remote_side=[id])
    children = relationship('Image', remote_side=[parent_id])

    def padded_id(self):
        """Returns the id padded with zeroes as a triple."""
        padded_id = '%09i' % self.id
        return (padded_id[0:3], padded_id[3:6], padded_id[6:9])


Index('images_parent_ix', Image.parent_id)
Index('images_owner_ix', Image.owner_id)
