import os

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..util import get_config_setting


@view_config(route_name='admin.sources.view.image')
@view_config(route_name='jokes.view.image')
def image(request):
    """Send the image data for a single source image."""
    image = None
    if request.matched_route.name == 'admin.sources.view.image' and request.current_user is not None:
        image = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                           Image.type == 'source')).first()
    if request.matched_route.name == 'jokes.view.image':
        image = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                           Image.type == 'joke')).first()
    if image:
        storage_path = get_config_setting(request, 'app.images.storage.path')
        if image and storage_path:
            return FileResponse(os.path.join(storage_path, *image.padded_id()),
                                request=request,
                                content_type=image.attributes['mimetype'][0])
    else:
        raise HTTPNotFound()
