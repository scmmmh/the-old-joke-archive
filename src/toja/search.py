from elasticsearch_dsl import connections, Document, Text

from .util import convert_type


class Joke(Document):
    """Elasticsearch document holding one joke."""
    
    text = Text()

    class Index:
        name = 'jokes'


def includeme(config):
    connections.create_connection(hosts=convert_type(config.get_settings()['app.elasticsearch.hosts'], 'list'))
