import math

from datetime import datetime
from pyramid.view import view_config

from ..config import SEARCH_FACETS
from ..models import Image
from ..search import JokeSearch

YEAR_FACETS = []
for facet in SEARCH_FACETS:
    if facet['type'] == 'date':
        YEAR_FACETS.append(facet['name'])


@view_config(route_name='search', renderer='toja:templates/search/index.jinja2')
def index(request):
    # Load parameters
    q = ''
    title = [(None, 'Jokes')]
    page = 0
    if 'q' in request.params and request.params['q'].strip() != '':
        q = request.params['q']
    if 'page' in request.params:
        try:
            page = max(0, int(request.params['page']))
        except ValueError:
            pass
    filters = {}
    if 'filter' in request.params:
        for value in request.params.getall('filter'):
            key, value = value.split(':')
            value = value.replace('%%%', ':')
            if key in YEAR_FACETS:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            if key in filters:
                filters[key].append(value)
            else:
                filters[key] = [value]

    # Process parameters
    if q:
        query = JokeSearch(q)
        title.append((None, 'containing'))
        title.append(('color-brand', q))
    else:
        query = JokeSearch(filters=filters)
        title.insert(0, (None, 'All'))
    query = query[page * 10:(page + 1) * 10]

    # Run search
    results = query.execute()
    joke_ids = [joke.meta.id for joke in results]
    jokes = request.dbsession.query(Image).filter(Image.id.in_(joke_ids))
    page_start = max(page - 2, 0)
    page_end = min(page_start + 5, math.ceil(results.hits.total.value / 10))
    page_start = max(page_end - 5, 0)
    return {'q': q,
            'pagination': {'start': page * 10 + 1,
                           'end': min(((page + 1) * 10), results.hits.total.value),
                           'total': results.hits.total.value,
                           'page': page,
                           'page_start': page_start,
                           'page_end': page_end},
            'jokes': jokes,
            'facets': results.facets,
            'title': title}
