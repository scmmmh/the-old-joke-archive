import os

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..util import get_config_setting


@view_config(route_name='source.image')
@view_config(route_name='joke.image')
def image(request):
    """Send the image data for a single image."""
    iid = None
    if request.matched_route.name == 'source.image':
        iid = request.matchdict['sid']
    elif request.matched_route.name == 'joke.image':
        iid = request.matchdict['jid']
    if iid:
        image = request.dbsession.query(Image).filter(and_(Image.id == iid,
                                                           Image.status != 'deleted')).first()
        if image is not None:
            storage_path = get_config_setting(request, 'app.images.storage.path')
            if image and storage_path:
                return FileResponse(os.path.join(storage_path, *image.padded_id()),
                                    request=request,
                                    content_type=image.attributes['mimetype'][0])
    raise HTTPNotFound()
