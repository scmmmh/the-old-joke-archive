from pyramid.view import view_config

from ..permissions import require_permission


@view_config(route_name='admin.index', renderer='toja:templates/admin/index.jinja2')
@require_permission('admin.view')
def index(request):
    """Admin landing page."""
    return {}
