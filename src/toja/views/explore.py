from elasticsearch import ConnectionError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config

from ..models import Image


@view_config(route_name='explore.recommend.mlt', renderer='toja:templates/explore/mlt.jinja2')
def recommend_mlt(request):
    """Recommend two more-like-this jokes for inclusion on another page."""
    try:
        search = Search(index='toja_jokes')
        search = search.query(MoreLikeThis(like={'_id': request.matchdict['jid']}))
        search = search[0:2]
        results = search.execute()
        joke_ids = [joke.meta.id for joke in results]
        if joke_ids and len(joke_ids) >= 2:
            jokes = request.dbsession.query(Image).filter(Image.id.in_(joke_ids))
            return {'jokes': jokes}
    except ConnectionError:
        pass
    raise HTTPNotFound()


@view_config(route_name='explore.recommend.random', renderer='toja:templates/explore/mlt.jinja2')
def recommend_random(request):
    """Recommend two random jokes for inclusion on another page."""
    try:
        search = Search.from_dict({'query': {'function_score': {'query': {'match_all': {}}, 'random_score': {}}}})
        search = search[0:2]
        results = search.execute()
        joke_ids = [joke.meta.id for joke in results]
        if joke_ids and len(joke_ids) >= 2:
            jokes = request.dbsession.query(Image).filter(Image.id.in_(joke_ids))
            return {'jokes': jokes}
    except ConnectionError:
        pass
    raise HTTPNotFound()
