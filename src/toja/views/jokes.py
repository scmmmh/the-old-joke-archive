from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..util import get_config_setting


@view_config(route_name='joke.view', renderer='toja:templates/jokes/view.jinja2')
def view(request):
    joke = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                      Image.type == 'joke',
                                                      Image.status == 'confirmed')).first()
    metadata_config = zip(get_config_setting(request, 'app.sources.metadata.fields', target_type='list'),
                          get_config_setting(request, 'app.sources.metadata.types', target_type='list'),
                          get_config_setting(request, 'app.sources.metadata.labels', target_type='list'))
    if joke:
        return {'joke': joke,
                'metadata_config': metadata_config}
    else:
        raise HTTPNotFound()
