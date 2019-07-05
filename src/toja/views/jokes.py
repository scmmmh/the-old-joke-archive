from pyramid.view import view_config


@view_config(route_name='joke.view', renderer='toja:templates/jokes/view.jinja2')
def view(request):
    return {}
