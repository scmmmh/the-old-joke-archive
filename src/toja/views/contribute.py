from pyramid.view import view_config


@view_config(route_name='contribute', renderer='toja:templates/contribute/index.jinja2')
def index(request):
    """Handle the contribution landing page."""
    return {}
