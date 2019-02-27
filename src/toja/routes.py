from pyramid_jinja2.filters import route_url_filter, static_url_filter


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('root', '/')

    config.add_route('users.list', '/users')
    config.add_route('users.register', '/users/register')
    config.add_route('users.confirm', '/users/confirm/:email/:token')
    config.add_route('users.login', '/users/login')
    config.add_route('users.logout', '/users/logout')
    config.add_route('users.edit.permissions', '/users/:uid/edit/permissions')
    config.add_route('users.edit.status', '/users/:uid/edit/status')
    config.add_route('users.edit.trust', '/users/:uid/edit/trust')
    config.add_route('users.delete', '/users/:uid/delete')

    config.add_route('sources.list', '/sources')
    config.add_route('sources.upload', '/sources/upload')
    config.add_route('sources.view.image', '/sources/:sid/image')
    config.add_route('sources.edit.attribute', '/sources/:sid/edit/:attribute')
    config.add_route('sources.delete', '/sources/:sid/delete')

    config.get_jinja2_environment().filters['static_url'] = static_url_filter
    config.get_jinja2_environment().filters['route_url'] = route_url_filter
