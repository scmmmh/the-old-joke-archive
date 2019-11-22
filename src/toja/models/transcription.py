from datetime import datetime
from sqlalchemy import (Column, Index, Integer, Unicode, ForeignKey, DateTime, Table)
from sqlalchemy.orm import relationship
from sqlalchemy_json import NestedMutableJson

from .meta import Base


class Transcription(Base):
    """The :class:`~toja.models.transcription.Transcription` represents a single transcription of a joke
    :class:`~toja.models.image.Image`.
    """

    __tablename__ = 'transcriptions'

    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('images.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    text = Column(NestedMutableJson)
    attributes = Column(NestedMutableJson)
    status = Column(Unicode(255))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=None, onupdate=datetime.now)

    source = relationship('Image')
    owner = relationship('User')

    def pure_text(self):
        """Returns just the text without any annotations."""
        def node_text(node):
            if node['type'] == 'text':
                return node['text']
            elif node['type'] == 'doc':
                return '\n'.join([node_text(child) for child in node['content']])
            else:
                return ''.join([node_text(child) for child in node['content']])
        return node_text(self.text)

    def to_jsonapi(self):
        """Returns a JSONAPI representation of this :class:`~toja.models.transcription.Transcription`."""
        attrs = {'source_id': self.source_id,
                 'owner_id': self.owner_id,
                 'text': self.text,
                 'status': self.status}
        attrs.update(self.attributes)
        return {'type': 'transcriptions',
                'id': self.id,
                'attributes': attrs}


Index('transcriptions_source_id_ix', Transcription.source_id)
Index('transcriptions_owner_id_ix', Transcription.owner_id)


transcription_links = Table('transcription_links', Base.metadata,
                            Column('source_id', Integer, ForeignKey('transcriptions.id'), primary_key=True),
                            Column('target_id', Integer, ForeignKey('transcriptions.id'), primary_key=True),
                            Column('relationship', Unicode(191), primary_key=True))
