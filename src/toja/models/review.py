from datetime import datetime
from sqlalchemy import (Column, Integer, ForeignKey, DateTime, Table)
from sqlalchemy.orm import relationship
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class Review(Base):

    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    attributes = Column(NestedMutableJson)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=None, onupdate=datetime.now)

    owner = relationship('User')


transcription_links = Table('images_reviews', Base.metadata,
                            Column('image_id', Integer, ForeignKey('images.id'), primary_key=True),
                            Column('review_id', Integer, ForeignKey('reviews.id'), primary_key=True))
