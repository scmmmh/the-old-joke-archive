from copy import deepcopy
from math import ceil
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..session import require_logged_in
from ..config import ANNOTATIONS, JOKE_METADATA
from ..translation import _


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
    annotations = []
    for annotation in ANNOTATIONS:
        annotation = deepcopy(annotation)
        if 'attrs' in annotation:
            for attr in annotation['attrs']:
                if 'values' in attr:
                    attr['values'] = [(value, _(request, value)) for value in attr['values']]
                if attr['type'] in ['singletext', 'multitext']:
                    attr['autosuggest'] = request.route_url('search.autosuggest', category=attr['name'])
        annotations.append(annotation)
    metadata = []
    for entry in JOKE_METADATA:
        if entry['type'] in ['multichoice', 'select']:
            metadata.append({'name': entry['name'],
                             'label': entry['label'],
                             'type': entry['type'],
                             'values': [(value, _(request, value)) for value in entry['values']]})
        elif entry['type'] == 'multitext':
            metadata.append({'name': entry['name'],
                             'label': entry['label'],
                             'type': entry['type'],
                             'autosuggest': request.route_url('search.autosuggest', category=entry['name'])})
    if request.current_user.trust == 'full':
        return {'config': {'baseURL': request.route_url('api'),
                           'sourceId': int(request.matchdict['sid']),
                           'userId': request.current_user.id,
                           'annotations': annotations,
                           'metadata': metadata}}
    else:
        raise HTTPForbidden()
