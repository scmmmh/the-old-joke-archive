def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('root', '/')

    config.add_route('users.register', '/users/register')
    config.add_route('users.confirm', '/users/confirm/:email/:token')
    config.add_route('users.login', '/users/login')
    config.add_route('users.logout', '/users/logout')
