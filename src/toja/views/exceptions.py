from pyramid.view import notfound_view_config, forbidden_view_config


@notfound_view_config(renderer='toja:templates/exceptions/404.jinja2')
def notfound_view(request):
    """Handle URLs that are not found."""
    request.response.status = 404
    return {}


@forbidden_view_config(renderer='toja:templates/exceptions/403.jinja2')
def forbidden_view(request):
    """Handle URLs that the user is forbidden from accessing."""
    request.response.status = 403
    return {}
