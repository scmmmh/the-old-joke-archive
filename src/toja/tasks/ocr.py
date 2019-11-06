import dramatiq
import os
import tesserocr

from PIL import Image as PILImage
from sqlalchemy import and_

from .middleware import ConfigMiddleware, DBSessionMiddleware
from toja.models import Image, Transcription


class OCRException(Exception):
    """Exception thrown during OCR processing. Details in the ``message`` attribute."""

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return "OCRException('{0}')".format(self.message)


@dramatiq.actor(min_backoff=500)
def run_ocr(jid):
    """Perform OCR using Tesseract on the :class:`~toja.models.image.Image` with the id ``jid`` and the type ``'joke'``.

    Creates a new :class:`~toja.models.transcription.Transcription` for the image with the OCRed text set as the
    text and a ``status`` of ``'ocr'``. If such a :class:`~toja.models.transcription.Transcription` already exists,
    then the text is updated instead.

    This is a dramatiq Actor, so can be run in the background.
    """
    storage_path = ConfigMiddleware.config_setting('app.images.storage.path')
    if storage_path:
        dbsession = DBSessionMiddleware.dbsession()
        joke = dbsession.query(Image).filter(and_(Image.id == jid, Image.type == 'joke')).first()
        if joke:
            transcription = dbsession.query(Transcription).filter(and_(Transcription.status == 'ocr',
                                                                       Transcription.source == joke)).first()
            if not transcription:
                transcription = Transcription(source=joke,
                                              text={'type': 'doc',
                                                    'content': [{'type': 'paragraph',
                                                                 'content': [{'type': 'text',
                                                                              'text': ''}]}]},
                                              status='ocr',
                                              attributes={})
            img = PILImage.open(os.path.join(storage_path, *joke.padded_id()))
            raw_text = tesserocr.image_to_text(img).strip().replace('--', '—')
            transcription.text = {'type': 'doc',
                                  'content': [{'type': 'paragraph',
                                               'content': [{'type': 'text',
                                                            'text': para.replace('\n', ' ')}]}
                                              for para in raw_text.split('\n\n')]}
            dbsession.add(transcription)
        else:
            raise OCRException("Joke not found in the database")
    else:
        raise OCRException("Missing configuration setting app.images.storage.path")
