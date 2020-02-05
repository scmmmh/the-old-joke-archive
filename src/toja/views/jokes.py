from pyramid.httpexceptions import HTTPNotFound, HTTPOk, HTTPBadRequest
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..session import require_logged_in
from ..tasks.joke import rate_joke as rate_joke_task
from ..util import Validator


@view_config(route_name='joke.view', renderer='toja:templates/jokes/view.jinja2')
def view(request):
    joke = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                      Image.type == 'joke',
                                                      Image.status.in_(('confirmed', 'final')))).first()
    if joke:
        return {'joke': joke}
    else:
        raise HTTPNotFound()


joke_rating_validator = {
    'rating': {'type': 'string', 'required': True, 'allowed': ['lol', 'groan', 'smile']}}


@view_config(route_name='joke.rate', renderer='json')
@require_logged_in()
def rate_joke(request):
    if request.method == 'POST':
        validator = Validator(joke_rating_validator)
        if validator.validate(request.params):
            rate_joke_task.send(request.matchdict['jid'], request.params['rating'], request.current_user.id)
            return HTTPOk()
        else:
            raise HTTPBadRequest()
    else:
        joke = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                          Image.type == 'joke',
                                                          Image.status.in_(('confirmed', 'final')))).first()
        if joke:
            if joke.attributes and 'ratings' in joke.attributes:
                return dict([(key, len(value)) for key, value in joke.attributes['ratings'].items()])
            else:
                return {}
        else:
            raise HTTPNotFound()
