import json

from base64 import urlsafe_b64encode, urlsafe_b64decode
from pyramid_jinja2.filters import route_url_filter, static_url_filter


def encode_route(request):
    """Jinja2 filter that returns the current route as a JSON object, which is then URL-safe base64 encoded."""
    if request.matched_route:
        data = {'route': request.matched_route.name,
                'params': request.matchdict,
                'query': list(request.params.items())}
        return urlsafe_b64encode(json.dumps(data).encode('utf-8')).decode()
    return None


def decode_route(request, default_route='root', default_route_params=None, default_route_query=None):
    """Jinja2 filter"""
    if 'redirect' in request.params and request.params['redirect']:
        try:
            data = json.loads(urlsafe_b64decode(request.params['redirect'].encode()).decode('utf-8'))
            return request.route_url(data['route'], **data['params'], _query=data['query'])
        except Exception:
            pass
    if not default_route_params:
        default_route_params = {}
    return request.route_url(default_route, **default_route_params, _query=default_route_query)


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/')

    config.add_route('user.register', '/users/register')
    config.add_route('user.confirm', '/users/confirm/:email/:token')
    config.add_route('user.login', '/users/login')
    config.add_route('user.logout', '/users/logout')
    config.add_route('user.view', '/users/:uid')

    config.add_route('search', '/search')

    config.add_route('contribute', '/contribute')
    config.add_route('contribute.sources', '/contribute/sources')
    config.add_route('contribute.workbench', '/contribute/workbench')

    config.add_route('joke.view', '/jokes/:jid')

    # Jinja2 configuration
    config.get_jinja2_environment().filters['static_url'] = static_url_filter
    config.get_jinja2_environment().filters['route_url'] = route_url_filter
    config.get_jinja2_environment().filters['encode_route'] = encode_route
    config.get_jinja2_environment().filters['decode_route'] = decode_route
