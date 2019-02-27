from pyramid.view import view_config

from ..models import Image


@view_config(route_name='crowdsourcing', renderer='toja:templates/crowdsourcing/index.jinja2')
def crowdsourcing(request):
    """Handles the crowdsourcing overview."""
    sources_count = request.dbsession.query(Image).filter(Image.type == 'source').count()
    return {'counts': {'sources': sources_count}}
