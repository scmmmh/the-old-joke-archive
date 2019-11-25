from elasticsearch_dsl import connections, Document, Text

from .util import convert_type


class Joke(Document):
    """Elasticsearch document holding one joke."""

    text = Text()

    class Index:
        name = 'jokes'


def update_search_param(request, parameter, new_value):
    params = []
    found = False
    for key in request.params.keys():
        if key == parameter:
            found = True
            params.append((key, new_value))
        else:
            for value in request.params.getall(key):
                params.append((key, value))
    if not found:
        params.append((parameter, new_value))
    return request.current_route_url(_query=params)


def includeme(config):
    connections.create_connection(hosts=convert_type(config.get_settings()['app.elasticsearch.hosts'], 'list'))

    # Jinja2 configuration
    config.get_jinja2_environment().filters['update_search_param'] = update_search_param
