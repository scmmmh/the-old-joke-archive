import os

from base64 import b64encode
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import and_

from toja.models import Image
from toja.permissions import require_permission
from toja.util import date_to_json, get_config_setting


def to_jsonapi(request, source):
    """Render a source :class:`~toja.models.image.Image` as JsonAPI."""
    storage_path = get_config_setting(request, 'app.images.storage.path')
    with open(os.path.join(storage_path, *source.padded_id()), 'rb') as in_f:
        raw_data = b64encode(in_f.read())
    attrs = {'status': source.status,
             'created': date_to_json(source.created),
             'updated': date_to_json(source.updated),
             'raw': 'data:{0};base64,{1}'.format(source.attributes['mimetype'], raw_data.decode('utf8'))}
    attrs.update(source.attributes)
    return {'type': 'sources',
            'id': source.id,
            'attributes': attrs}


@view_config(route_name='api.source.get', renderer='json')
@require_permission('sources.admin or @view user :sid')
def source_get(request):
    """GET a single source :class:`~toja.models.image.Image`."""
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source')).first()
    if source:
        return {'data': to_jsonapi(request, source)}
    else:
        raise HTTPNotFound()
