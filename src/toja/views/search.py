from pyramid.view import view_config


@view_config(route_name='search', renderer='toja:templates/search/index.jinja2')
def index(request):
    return {}
