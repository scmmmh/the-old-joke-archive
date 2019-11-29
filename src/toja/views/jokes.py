from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image


@view_config(route_name='joke.view', renderer='toja:templates/jokes/view.jinja2')
def view(request):
    joke = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                      Image.type == 'joke',
                                                      Image.status == 'confirmed')).first()
    if joke:
        return {'joke': joke}
    else:
        raise HTTPNotFound()
