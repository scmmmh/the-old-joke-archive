def includeme(config):
    if 'app.testing' in config.get_settings() and config.get_settings()['app.testing'].lower().strip() == 'true':
        config.add_route('tests.create', '/tests/create')
        config.add_view('toja.tests.views.create', route_name='tests.create', renderer='json')
