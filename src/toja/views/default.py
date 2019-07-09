from pyramid.view import view_config


@view_config(route_name='root', renderer='toja:templates/root.jinja2')
def root(request):
    """Main landing page."""
    return {}


def dashboard(request):
    """Logged in user landing page."""
    return {}
