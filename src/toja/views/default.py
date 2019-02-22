from pyramid.view import view_config


@view_config(route_name='root', renderer='../templates/root.jinja2')
def root(request):
    return {}
