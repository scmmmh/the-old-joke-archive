import math

from pyramid.view import view_config

from ..search import JokeSearch
from ..models import Image


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

    # Process parameters
    if q:
        query = JokeSearch(q)
        title.append((None, 'containing'))
        title.append(('color-brand', q))
    else:
        query = JokeSearch()
        title.insert(0, (None, 'All'))

    # Run search
    query = query[page * 10:(page + 1) * 10]
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
