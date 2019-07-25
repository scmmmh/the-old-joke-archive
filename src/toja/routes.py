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
    """Jinja2 filter that decodes and returns the route URL encoded with :func:`~toja.routes.encode_route`."""
    if 'redirect' in request.params and request.params['redirect']:
        try:
            data = json.loads(urlsafe_b64decode(request.params['redirect'].encode()).decode('utf-8'))
            return request.route_url(data['route'], **data['params'], _query=data['query'])
        except Exception:
            pass
    if not default_route_params:
        default_route_params = {}
    return request.route_url(default_route, **default_route_params, _query=default_route_query)


def update_current_route(request, params=None, query=None):
    """Update the current route with new parameters or query."""
    if query:
        tmp = []
        for key in request.params.keys():
            if key in query:
                tmp.append((key, query[key]))
            else:
                for val in request.params.getall(key):
                    tmp.append((key, val))
        for key, value in query.items():
            tmp.append((key, value))
        query = tmp
    if params and query:
        return request.current_route_url(**params, _query=query)
    elif params:
        return request.current_route_url(**params)
    elif query:
        return request.current_route_url(_query=query)
    else:
        return request.current_route_url()


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/')

    config.add_route('user.index', '/users')
    config.add_route('user.register', '/users/register')
    config.add_route('user.confirm', '/users/confirm/:email/:token')
    config.add_route('user.login', '/users/login')
    config.add_route('user.logout', '/users/logout')
    config.add_route('user.forgotten_password', '/users/forgotten_password')
    config.add_route('user.view', '/users/:uid')
    config.add_route('user.edit', '/users/:uid/edit')
    config.add_route('user.delete', '/users/:uid/delete', request_method='POST')

    config.add_route('search', '/search')

    config.add_route('contribute', '/contribute')
    config.add_route('contribute.sources', '/contribute/sources')
    config.add_route('contribute.workbench', '/contribute/workbench')
    config.add_route('contribute.workbench.edit', '/contribute/workbench/:sid')

    config.add_route('joke.view', '/jokes/:jid')
    config.add_route('joke.image', '/jokes/:jid/image')

    config.add_route('source.index', '/sources')
    config.add_route('source.view', '/sources/:sid')
    config.add_route('source.image', '/sources/:sid/image')
    config.add_route('source.edit', '/sources/:sid/edit')
    config.add_route('source.delete', '/sources/:sid/delete', request_method='POST')

    config.add_route('admin.index', '/admin')

    config.add_route('api', '/api')
    config.add_route('api.sources.get', '/api/sources', request_method='GET')
    config.add_route('api.sources.post', '/api/sources', request_method='POST')
    config.add_route('api.source.get', '/api/sources/:sid', request_method='GET')
    config.add_route('api.source.put', '/api/sources/:sid', request_method='PUT')
    config.add_route('api.source.delete', '/api/sources/:sid', request_method='DELETE')
    config.add_route('api.jokes.get', '/api/sources/:sid/jokes', request_method='GET')
    config.add_route('api.jokes.post', '/api/sources/:sid/jokes', request_method='POST')
    config.add_route('api.joke.get', '/api/sources/:sid/jokes/:jid', request_method='GET')
    config.add_route('api.joke.put', '/api/sources/:sid/jokes/:jid', request_method='PUT')
    config.add_route('api.joke.delete', '/api/sources/:sid/jokes/:jid', request_method='DELETE')

    # Jinja2 configuration
    config.get_jinja2_environment().filters['static_url'] = static_url_filter
    config.get_jinja2_environment().filters['route_url'] = route_url_filter
    config.get_jinja2_environment().filters['encode_route'] = encode_route
    config.get_jinja2_environment().filters['decode_route'] = decode_route
    config.get_jinja2_environment().filters['update_current_route'] = update_current_route
