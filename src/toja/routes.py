from pyramid_jinja2.filters import route_url_filter, static_url_filter


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('root', '/')

    # Jinja2 configuration
    config.get_jinja2_environment().filters['static_url'] = static_url_filter
    config.get_jinja2_environment().filters['route_url'] = route_url_filter
