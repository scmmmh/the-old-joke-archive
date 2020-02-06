import dramatiq
import hashlib

from sqlalchemy import and_

from .middleware import DBSessionMiddleware
from ..config import SOURCE_METADATA, JOKE_METADATA, ANNOTATIONS
from ..models import Image
from ..search import Joke, Autosuggest
from ..util import extract_text, extract_annotations


@dramatiq.actor()
def index_all():
    """Index all jokes that have a final :class:`~toja.models.transcription.Transcription`.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    for joke in dbsession.query(Image).filter(Image.type == 'joke'):
        index_joke(joke.id)


@dramatiq.actor()
def index_joke(jid):
    """Index a single joke :class:`~toja.models.image.Image` with the id `jid`.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    db_joke = dbsession.query(Image).filter((and_(Image.id == jid,
                                                  Image.type == 'joke',
                                                  Image.status == 'final'))).first()
    if db_joke and 'text' in db_joke.attributes:
        joke = Joke(text=extract_text(db_joke.attributes['text']),
                    meta={'id': db_joke.id})
        for field in SOURCE_METADATA:
            value = db_joke.attribute('source.{0}'.format(field['name']))
            if value:
                if field['type'] == 'date':
                    if len(value.split('-')) < 3:
                        value = '{0}{1}'.format(value, '-01' * (3 - len(value.split('-'))))
                joke[field['name']] = value
        for field in JOKE_METADATA:
            if field['name'] in db_joke.attributes:
                joke[field['name']] = db_joke.attributes[field['name']]
                if field['type'] == 'multitext':
                    # Index auto-suggestion values
                    for value in db_joke.attributes[field['name']]:
                        m = hashlib.sha256()
                        m.update('{0}-{1}'.format(field['name'], value).encode('utf-8'))
                        autosuggest = Autosuggest(category=field['name'],
                                                  value=value,
                                                  value_suggests=value,
                                                  meta={'id': m.hexdigest()})
                        autosuggest.save()
        for annotation in ANNOTATIONS:
            if 'attrs' in annotation:
                annotations = extract_annotations(db_joke.attributes['text'], annotation['name'])
                for field in annotation['attrs']:
                    for entry in annotations:
                        if 'marks' in entry:
                            for mark in entry['marks']:
                                if 'attrs' in mark and 'settings' in mark['attrs'] and \
                                        field['name'] in mark['attrs']['settings']:
                                    if field['type'] == 'multitext':
                                        for value in mark['attrs']['settings'][field['name']]:
                                            m = hashlib.sha256()
                                            m.update('{0}-{1}'.format(field['name'], value).encode('utf-8'))
                                            autosuggest = Autosuggest(category=field['name'],
                                                                      value=value,
                                                                      value_suggests=value,
                                                                      meta={'id': m.hexdigest()})
                                            autosuggest.save()
                                    if field['type'] == 'singletext':
                                        value = mark['attrs']['settings'][field['name']]
                                        m = hashlib.sha256()
                                        m.update('{0}-{1}'.format(field['name'], value).encode('utf-8'))
                                        autosuggest = Autosuggest(category=field['name'],
                                                                  value=value,
                                                                  value_suggests=value,
                                                                  meta={'id': m.hexdigest()})
                                        autosuggest.save()
        joke.save()
    else:
        try:
            db_joke = Joke.get(id=jid)
            db_joke.delete()
        except Exception:
            pass
