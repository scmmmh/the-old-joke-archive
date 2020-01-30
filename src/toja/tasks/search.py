import dramatiq

from sqlalchemy import and_

from .middleware import DBSessionMiddleware
from ..models import Transcription
from ..search import Joke
from ..config import SOURCE_METADATA, JOKE_METADATA


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
        for field in SOURCE_METADATA:
            value = transcription.source.attribute('source.{0}'.format(field['name']))
            if value:
                if field['type'] == 'date':
                    if len(value.split('-')) < 3:
                        value = '{0}{1}'.format(value, '-01' * (3 - len(value.split('-'))))
                joke[field['name']] = value
        for field in JOKE_METADATA:
            if field['name'] in transcription.attributes:
                if 'values' in field:
                    value = transcription.attributes[field['name']]
                    if isinstance(value, list):
                        joke[field['name']] = []
                        for sub_value in value:
                            for config_value in field['values']:
                                if config_value['name'] == sub_value:
                                    joke[field['name']].append(config_value['label'])
                    else:
                        for config_value in field['values']:
                            if config_value['name'] == value:
                                joke[field['name']] = config_value['label']
                else:
                    joke[field['name']] = transcription.attributes[field['name']]
        joke.save()
