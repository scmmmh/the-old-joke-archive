from datetime import datetime
from sqlalchemy import (Column, Index, Integer, Unicode, ForeignKey, DateTime, Table)
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class Transcription(Base):

    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('images.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    text = Column(NestedMutableJson)
    attributes = Column(NestedMutableJson)
    status = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=None, onupdate=datetime.now)


Index('transcriptions_source_id_ix', Transcription.source_id)
Index('transcriptions_owner_id_ix', Transcription.owner_id)


transcription_links = Table('transcription_links', Base.metadata,
                            Column('source_id', Integer, ForeignKey('transcriptions.id'), primary_key=True),
                            Column('target_id', Integer, ForeignKey('transcriptions.id'), primary_key=True),
                            Column('relationship', Unicode(191), primary_key=True))
