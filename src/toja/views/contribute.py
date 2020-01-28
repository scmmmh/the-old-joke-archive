from math import ceil
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..session import require_logged_in
from ..config import ANNOTATIONS, JOKE_METADATA


@view_config(route_name='contribute', renderer='toja:templates/contribute/index.jinja2')
def index(request):
    """Handle the contribution landing page."""
    return {}


@view_config(route_name='contribute.workbench', renderer='toja:templates/contribute/workbench/index.jinja2')
@require_logged_in()
def workbench(request):
    """Handle the source overview list for the transcription workbench."""
    if request.current_user.trust == 'full':
        try:
            page = int(request.params['page'])
        except Exception:
            page = 0
        sources = request.dbsession.query(Image).filter(and_(Image.type == 'source',
                                                             Image.status == 'processing'))
        total = sources.count()
        sources = sources.offset(page * 10).limit(10)
        return {'sources': sources,
                'pagination': {'start': max(0, page - 2),
                               'current': page,
                               'end': min(ceil(total / 10), page + 2),
                               'total': total}}
    else:
        raise HTTPForbidden()


@view_config(route_name='contribute.workbench.edit', renderer='toja:templates/contribute/workbench/edit.jinja2')
@require_logged_in()
def workbench_edit(request):
    """Handle the transcription workbench page for a single source."""
    if request.current_user.trust == 'full':
        return {'config': {'baseURL': request.route_url('api'),
                           'sourceId': int(request.matchdict['sid']),
                           'userId': request.current_user.id,
                           'annotations': ANNOTATIONS,
                           'metadata': JOKE_METADATA}}
    else:
        raise HTTPForbidden()
