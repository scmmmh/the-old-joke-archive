import os

from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import FileResponse
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..session import require_logged_in
from ..util import get_config_setting


@view_config(route_name='jokes.view.image')
@require_logged_in()
def image(request):
    """Send the image data for a single source image."""
    image = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                       Image.type == 'joke')).first()
    print(image)
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if image and storage_path:
        padded_id = '%09i' % image.id
        padded_id = (padded_id[0:3], padded_id[3:6], padded_id[6:9])
        path = os.path.join(storage_path, *padded_id)
        return FileResponse(path, request=request, content_type=image.attributes['mimetype'][0])
    else:
        raise HTTPNotFound()
