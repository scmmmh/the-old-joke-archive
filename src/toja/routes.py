from pyramid_jinja2.filters import route_url_filter, static_url_filter


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('root', '/')

    # User routes
    config.add_route('users.list', '/users')
    config.add_route('users.register', '/users/register')
    config.add_route('users.confirm', '/users/confirm/:email/:token')
    config.add_route('users.login', '/users/login')
    config.add_route('users.logout', '/users/logout')
    config.add_route('users.edit.permissions', '/users/:uid/edit/permissions')
    config.add_route('users.edit.status', '/users/:uid/edit/status')
    config.add_route('users.edit.trust', '/users/:uid/edit/trust')
    config.add_route('users.delete', '/users/:uid/delete')

    # Admin routes
    # Admin sources routes
    config.add_route('admin.sources.list', '/admin/sources')
    config.add_route('admin.sources.upload', '/admin/sources/upload')
    config.add_route('admin.sources.edit.status', '/admin/sources/:sid/edit/status')
    config.add_route('admin.sources.edit.attribute', '/admin/sources/:sid/edit/:attribute')
    config.add_route('admin.sources.delete', '/admin/sources/:sid/delete')

    # Crowdsourcing routes
    config.add_route('crowdsourcing', '/contribute')
    # Crowdsourcing joke extraction routes
    config.add_route('crowdsourcing.identify', '/contribute/identify-jokes')
    config.add_route('crowdsourcing.identify.app', '/contribute/identify-jokes/:sid')
    config.add_route('crowdsourcing.identify.new', '/contribute/identify-jokes/:sid/create', request_method='POST')
    config.add_route('crowdsourcing.identify.update', '/contribute/identify-jokes/:sid/:jid/update',
                     request_method='PATCH')
    config.add_route('crowdsourcing.identify.delete', '/contribute/identify-jokes/:sid/:jid/delete',
                     request_method='DELETE')
    # Crowdsourcing joke verification routes
    config.add_route('crowdsourcing.verify_jokes', '/contribute/verify-jokes')
    config.add_route('crowdsourcing.verify_joke', '/contribute/verify-jokes/:jid', request_method='POST')
    # Crowdsourcing joke transcription routes
    config.add_route('crowdsourcing.transcribe_joke', '/contribute/transcribe-joke/:jid')

    # Image display routes
    config.add_route('images.view', '/images/:iid')

    # Jinja2 configuration
    config.get_jinja2_environment().filters['static_url'] = static_url_filter
    config.get_jinja2_environment().filters['route_url'] = route_url_filter
