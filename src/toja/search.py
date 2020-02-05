from datetime import timedelta
from elasticsearch_dsl import (connections, Document, Text, Keyword, Date, FacetedSearch, TermsFacet,
                               DateHistogramFacet, Completion)

from .util import convert_type


class Joke(Document):
    """Elasticsearch document holding one joke."""

    text = Text()
    type = Keyword(multi=True)
    topic = Keyword(multi=True)
    language = Keyword()
    pub_type = Keyword()
    pub_title = Keyword()
    pub_section = Keyword()
    pub_date = Date()

    class Index:
        name = 'toja_jokes'


class Autosuggest(Document):
    """Elasticsearch document holding one autosuggest value."""

    category = Keyword()
    value = Completion()

    class Index:
        name = 'toja_autosuggests'


class YearDateHistogramFacet(DateHistogramFacet):
    """Extended :class:`~elasticsearch_dsl.faceted_search.DateHistogramFacet` with support for year-long intervals."""

    DATE_INTERVALS = {
        'year': lambda d: (d+timedelta(days=367)).replace(day=1),
        'month': lambda d: (d+timedelta(days=32)).replace(day=1),
        'week': lambda d: d+timedelta(days=7),
        'day': lambda d: d+timedelta(days=1),
        'hour': lambda d: d+timedelta(hours=1),
    }


class JokeSearch(FacetedSearch):
    """Faceted search helper."""

    doc_types = (Joke, )
    fields = ['text']
    facets = {
        'type': TermsFacet(field='type'),
        'topic': TermsFacet(field='topic'),
        'language': TermsFacet(field='language'),
        'pub_title': TermsFacet(field='pub_title'),
        'pub_type': TermsFacet(field='pub_type'),
        'pub_section': TermsFacet(field='pub_section'),
        'pub_date': YearDateHistogramFacet(field='pub_date', interval='month'),
    }


def update_search_param(request, parameter, new_value):
    """Update the request ``parameter`` with a ``new_value``, overwriting any existing value."""
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


def add_search_param(request, parameter, new_value):
    """Add a new ``parameter`` with the given ``new_vale``. If the combination already exists, then nothing is changed.
    Any ``parameter`` parameters with different values are left as they were."""
    params = []
    found = False
    for key, value in request.params.items():
        if key == parameter and value == new_value:
            found = True
        params.append((key, value))
    if not found:
        params.append((parameter, new_value))
    return request.current_route_url(_query=params)


def remove_search_param(request, parameter, old_value):
    """Remove a ``parameter`` with the given ``old_vale``. If the combination does not exist, then nothing is changed.
    Any ``parameter`` parameters with different values are left as they were."""
    params = []
    for key, value in request.params.items():
        if key != parameter or value != old_value:
            params.append((key, value))
    return request.current_route_url(_query=params)


def includeme(config):
    connections.create_connection(hosts=convert_type(config.get_settings()['app.elasticsearch.hosts'], 'list'))

    # Jinja2 configuration
    config.get_jinja2_environment().filters['update_search_param'] = update_search_param
    config.get_jinja2_environment().filters['add_search_param'] = add_search_param
    config.get_jinja2_environment().filters['remove_search_param'] = remove_search_param
