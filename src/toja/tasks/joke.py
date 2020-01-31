import dramatiq

from sqlalchemy import and_

from .middleware import DBSessionMiddleware
from .search import index_joke
from ..config import JOKE_METADATA
from ..models import Image
from ..util import extract_annotations, extract_text


@dramatiq.actor()
def process_joke(jid):
    """Process a single joke :class:`~toja.models.transcription.Source` with the id
    `jid`.

    This is a dramatiq Actor, so can be run in the background.
    """
    dbsession = DBSessionMiddleware.dbsession()
    joke = dbsession.query(Image).filter(and_(Image.id == jid, Image.type == 'joke')).first()
    if joke:
        if len([t for t in joke.transcriptions if t.status == 'final']) == 1:
            transcription = [t for t in joke.transcriptions if t.status == 'final'][0]
            joke.attributes['text'] = transcription.text
            for field in JOKE_METADATA:
                if field['type'] in ['multichoice', 'select'] and field['name'] in transcription.attributes:
                    if 'values' in field:
                        value = transcription.attributes[field['name']]
                        if isinstance(value, list):
                            joke.attributes[field['name']] = []
                            for sub_value in value:
                                for config_value in field['values']:
                                    if config_value['name'] == sub_value:
                                        joke.attributes[field['name']].append(config_value['label'])
                        else:
                            for config_value in field['values']:
                                if config_value['name'] == value:
                                    joke.attributes[field['name']] = config_value['label']
                    else:
                        joke.attributes[field['name']] = transcription.attributes[field['name']]
                elif field['type'] == 'extract-single':
                    annotations = extract_annotations(transcription.text, field['source']['type'])
                    if annotations:
                        if field['source']['attr'] == 'text':
                            joke.attributes[field['name']] = ', '.join([extract_text(annotation)
                                                                        for annotation in annotations])
    index_joke.send_with_options(kwargs={'jid': jid}, delay=1000)
