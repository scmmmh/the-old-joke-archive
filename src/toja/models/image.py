from datetime import datetime
from jinja2 import Undefined
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
    children = relationship('Image',
                            primaryjoin="and_(Image.id == remote(Image.parent_id), "
                                        "Image.status != 'deleted')",
                            cascade="all,delete,delete-orphan")
    transcriptions = relationship('Transcription',
                                  order_by='desc(Transcription.created)')
    transcription = relationship('Transcription',
                                 primaryjoin="and_(Image.id == Transcription.source_id, "
                                             "Transcription.status == 'final')",
                                 uselist=False)
    # reviews = relationship('Review', secondary='images_reviews')

    def attribute(self, path):
        if path:
            if path.startswith('source.'):
                if self.parent:
                    return self.parent.attribute(path[7:])
                else:
                    return Undefined(name=path)
            else:
                if path in self.attributes:
                    return self.attributes[path]
                else:
                    return Undefined(name=path)
        else:
            return Undefined()

    def padded_id(self):
        """Returns the id padded with zeroes as a triple."""
        padded_id = '%09i' % self.id
        return (padded_id[0:3], padded_id[3:6], padded_id[6:9])

    def allow(self, user, action):
        """Check if the given user is allowed the given action.

        :param user: The user to check the permission for
        :type user: :class:`~toja.models.user.User`
        :param action: The action to check (view, edit, delete)
        :type action: `str`
        :return: Whether the user is allowed the action
        :return_type: `boolean`
        """
        if action == 'view':
            return True
        elif action == 'edit':
            return user is not None and user.id == self.owner_id
        elif action == 'delete':
            return user is not None and user.id == self.owner_id


Index('images_parent_ix', Image.parent_id)
Index('images_owner_ix', Image.owner_id)
