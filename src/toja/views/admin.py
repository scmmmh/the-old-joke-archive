from elasticsearch_dsl import Index
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from ..permissions import require_permission
from ..search import Joke
from ..tasks import index_all


@view_config(route_name='admin.index', renderer='toja:templates/admin/index.jinja2')
@require_permission('admin.view')
def index(request):
    """Admin landing page."""
    return {}


@view_config(route_name='admin.search', renderer='toja:templates/admin/search.jinja2')
@require_permission('admin.search')
def search(request):
    """Search Admin landing page."""
    types = [('Jokes', Joke)]
    indices = [(t[0], Index(name=t[1].Index.name)) for t in types]
    if request.method == 'POST':
        if 'action' in request.params:
            if request.params['action'] == 'create':
                for index in indices:
                    if index[1].exists():
                        index[1].delete()
                for es_type in types:
                    es_type[1].init()
                index_all.send()
            elif request.params['action'] == 'index':
                index_all.send()
        return HTTPFound(request.route_url('admin.search'))
    indices = [(index[0], index[1], index[1].stats() if index[1].exists() else None) for index in indices]
    return {'indices': indices}
