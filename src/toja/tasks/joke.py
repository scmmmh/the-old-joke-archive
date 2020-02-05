import dramatiq

from sqlalchemy import and_

from .middleware import DBSessionMiddleware, RateLimiterMiddleware
from .search import index_joke
from ..config import JOKE_METADATA
from ..models import Image
from ..util import extract_annotations, extract_text


@dramatiq.actor()
def process_all_jokes():
    """Process all jokes.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    for joke in dbsession.query(Image).filter(Image.type == 'joke'):
        process_joke.send(joke.id)


@dramatiq.actor()
def process_joke(jid):
    """Process a single joke :class:`~toja.models.image.Image` with the id
    `jid`.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    joke = dbsession.query(Image).filter(and_(Image.id == jid, Image.type == 'joke')).first()
    if joke:
        if len([t for t in joke.transcriptions if t.status == 'final']) == 1:
            transcription = [t for t in joke.transcriptions if t.status == 'final'][0]
            joke.attributes['text'] = transcription.text
            joke.status = 'final'
            for field in JOKE_METADATA:
                if field['type'] in ['multichoice', 'select'] and field['name'] in transcription.attributes:
                    if field['name'] in transcription.attributes:
                        joke.attributes[field['name']] = transcription.attributes[field['name']]
                elif field['type'] == 'extract-single':
                    annotations = extract_annotations(transcription.text, field['source']['type'])
                    if annotations:
                        if field['source']['attr'] == 'text':
                            joke.attributes[field['name']] = ', '.join([extract_text(annotation)
                                                                        for annotation in annotations])
    index_joke.send_with_options(kwargs={'jid': jid}, delay=1000)


@dramatiq.actor()
def rate_joke(jid, rating, uid):
    """Rate a single joke :class:`~toja.models.image.Image`, ensuring that a single user only rates once."""
    with RateLimiterMiddleware.get_rate_limiter('joke-rating').acquire():
        dbsession = DBSessionMiddleware.dbsession()
        joke = dbsession.query(Image).filter(and_(Image.id == jid, Image.type == 'joke')).first()
        if joke:
            if 'ratings' not in joke.attributes:
                joke.attributes['ratings'] = {}
            if rating not in joke.attributes['ratings']:
                joke.attributes['ratings'][rating] = []
            for key, value in joke.attributes['ratings'].items():
                if key != rating:
                    while uid in value:
                        value.remove(uid)
            if uid not in joke.attributes['ratings'][rating]:
                joke.attributes['ratings'][rating].append(uid)
