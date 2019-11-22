import dramatiq

from sqlalchemy import and_

from .middleware import DBSessionMiddleware
from ..models import Transcription
from ..search import Joke


@dramatiq.actor()
def index_all():
    """Index all jokes that have a final :class:`~toja.models.transcription.Transcription`.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    for transcription in dbsession.query(Transcription).filter(Transcription.status == 'final'):
        index_joke.send(transcription.id)


@dramatiq.actor()
def index_joke(tid):
    """Index a single joke identified through the final :class:`~toja.models.transcription.Transcription` with the id
    `tid`.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    transcription = dbsession.query(Transcription).filter(and_(Transcription.id == tid,
                                                               Transcription.status == 'final')).first()
    if transcription:
        joke = Joke(text=transcription.pure_text(),
                    meta={'id': transcription.source.id})
        joke.save()
