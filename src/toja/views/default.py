from elasticsearch import ConnectionError
from elasticsearch_dsl import Search
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..search import Joke


@view_config(route_name='root', renderer='toja:templates/root.jinja2')
def root(request):
    """Main landing page."""
    total_joke_count = request.dbsession.query(Image).filter(Image.type == 'joke').count()
    transcribed_joke_count = request.dbsession.query(Image).filter(and_(Image.type == 'joke',
                                                                        Image.status == 'final')).count()
    joke = None
    try:
        search = Search.from_dict({'query': {'function_score': {'query': {'match_all': {}}, 'random_score': {}}}})
        search.index(Joke.Index.name)
        search = search[0]
        results = search.execute()
        if len(results) == 1:
            joke = request.dbsession.query(Image).filter(and_(Image.id == results[0].meta.id,
                                                              Image.type == 'joke')).first()
    except ConnectionError:
        pass
    return {'total_joke_count': total_joke_count,
            'transcribed_joke_count': transcribed_joke_count,
            'joke': joke}


def dashboard(request):
    """Logged in user landing page."""
    return {}
