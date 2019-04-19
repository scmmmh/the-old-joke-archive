import os

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config

from ..models import Image
from ..util import get_config_setting


@view_config(route_name='images.view')
def image(request):
    """Send the image data for a single source image."""
    image = request.dbsession.query(Image).filter(Image.id == request.matchdict['iid']).first()
    if image is not None:
        if image.type == 'joke' or (image.type == 'source' and request.current_user is not None):
            storage_path = get_config_setting(request, 'app.images.storage.path')
            if image and storage_path:
                return FileResponse(os.path.join(storage_path, *image.padded_id()),
                                    request=request,
                                    content_type=image.attributes['mimetype'][0])
    raise HTTPNotFound()
