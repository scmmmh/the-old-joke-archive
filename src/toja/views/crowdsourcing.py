from pyramid.view import view_config


@view_config(route_name='crowdsourcing', renderer='toja:templates/crowdsourcing/index.jinja2')
def crowdsourcing(request):
    return {}
