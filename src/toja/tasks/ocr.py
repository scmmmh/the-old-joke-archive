import os

from ..celery import app
from PIL import Image as PillowImage
from pytesseract import image_to_string
from sqlalchemy import and_

from .base import ConfiguredTask
from ..models import Image


@app.task(bind=True, base=ConfiguredTask)
def ocr_single_image(self, imageid):
    """OCR a single image, if it has the "confirmed" status."""
    dbsession = self.dbsession
    image = dbsession.query(Image).filter(and_(Image.id == imageid,
                                               Image.type == 'joke',
                                               Image.status == 'confirmed')).first()
    if image is not None and 'app.images.storage.path' in self._settings:
        storage_path = self._settings['app.images.storage.path']
        image_to_string(PillowImage.open(os.path.join(storage_path, *image.padded_id())))
    dbsession.close()
