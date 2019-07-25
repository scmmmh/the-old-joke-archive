from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import and_

from toja.models import Image
from toja.permissions import require_permission
from toja.util import date_to_json


def to_jsonapi(request, source):
    """Render a source :class:`~toja.models.image.Image` as JsonAPI."""
    attrs = {'status': source.status,
             'created': date_to_json(source.created),
             'updated': date_to_json(source.updated),
             'raw': request.route_url('source.image', sid=source.id)}
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
