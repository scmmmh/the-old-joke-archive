import json
import os

from PIL import Image as PILImage
from pyramid.httpexceptions import HTTPNotFound, HTTPOk
from pyramid.view import view_config
from random import sample
from sqlalchemy import and_

from ..models import Image
from ..util import get_config_setting
from ..session import require_logged_in


@view_config(route_name='crowdsourcing', renderer='toja:templates/crowdsourcing/index.jinja2')
def crowdsourcing(request):
    """Handles the crowdsourcing overview."""
    sources_count = request.dbsession.query(Image).filter(Image.type == 'source').count()
    return {'counts': {'sources': sources_count}}


@view_config(route_name='crowdsourcing.identify', renderer='toja:templates/crowdsourcing/identify_jokes_tasks.jinja2')
@require_logged_in()
def identify_jokes_tasks(request):
    """Show a random list of 10 source tasks to the user."""
    task_ids = [i.id for i in request.dbsession.query(Image.id).filter(and_(Image.type == 'source',
                                                                            Image.status == 'processing'))]
    task_ids = sample(task_ids, min(len(task_ids), 10))
    tasks = request.dbsession.query(Image).filter(Image.id.in_(task_ids))
    metadata = list(zip(get_config_setting(request, 'app.sources.metadata.fields', target_type='list', default=[]),
                        get_config_setting(request, 'app.sources.metadata.types', target_type='list', default=[]),
                        get_config_setting(request, 'app.sources.metadata.labels', target_type='list', default=[])))
    return {'tasks': tasks,
            'metadata': metadata}


@view_config(route_name='crowdsourcing.identify.app', renderer='toja:templates/crowdsourcing/identify_jokes_app.jinja2')
@require_logged_in()
def identify_jokes_app(request):
    """Show the joke extraction app."""
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source')).first()
    if source:
        return {'source': source}
    else:
        raise HTTPNotFound()


@view_config(route_name='crowdsourcing.identify.new', renderer='json')
@require_logged_in()
def create_new_joke(request):
    """Create a new extracted joke."""
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source')).first()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if source and storage_path:
        body = json.loads(request.body)
        source_img = PILImage.open(os.path.join(storage_path, *source.padded_id()))
        joke_img = Image(owner=request.current_user,
                         parent=source,
                         attributes={'mimetype': 'image/jpeg',
                                     'bbox': body['data']['attributes']['bbox']},
                         type='joke',
                         status='new')
        request.dbsession.add(joke_img)
        request.dbsession.flush()
        part_img = source_img.crop((int(body['data']['attributes']['bbox']['left']),
                                    int(body['data']['attributes']['bbox']['top']),
                                    int(body['data']['attributes']['bbox']['left']) +
                                    int(body['data']['attributes']['bbox']['width']),
                                    int(body['data']['attributes']['bbox']['top']) +
                                    int(body['data']['attributes']['bbox']['height'])))
        part_img.save(os.path.join(storage_path, *joke_img.padded_id()), format='jpeg')
        return {'data': {'types': 'images',
                         'id': joke_img.id,
                         'attributes': joke_img.attributes}}
    else:
        raise HTTPNotFound()


@view_config(route_name='crowdsourcing.identify.update', renderer='json')
@require_logged_in()
def update_joke(request):
    """Update an extracted joke."""
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source')).first()
    joke_img = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                          Image.type == 'joke',
                                                          Image.parent_id == source.id,
                                                          Image.owner_id == request.current_user.id)).first()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if source and joke_img and storage_path:
        body = json.loads(request.body)
        source_img = PILImage.open(os.path.join(storage_path, *source.padded_id()))
        joke_img.attributes['bbox'] = body['data']['attributes']['bbox']
        request.dbsession.add(joke_img)
        request.dbsession.flush()
        part_img = source_img.crop((int(body['data']['attributes']['bbox']['left']),
                                    int(body['data']['attributes']['bbox']['top']),
                                    int(body['data']['attributes']['bbox']['left']) +
                                    int(body['data']['attributes']['bbox']['width']),
                                    int(body['data']['attributes']['bbox']['top']) +
                                    int(body['data']['attributes']['bbox']['height'])))
        part_img.save(os.path.join(storage_path, *joke_img.padded_id()), format='jpeg')
        return {'data': {'types': 'images',
                         'id': joke_img.id,
                         'attributes': joke_img.attributes}}
    else:
        raise HTTPNotFound()


@view_config(route_name='crowdsourcing.identify.delete', renderer='json')
@require_logged_in()
def delete_joke(request):
    """Update an extracted joke."""
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source')).first()
    joke_img = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                          Image.type == 'joke',
                                                          Image.parent_id == source.id,
                                                          Image.owner_id == request.current_user.id)).first()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if source and joke_img and storage_path:
        try:
            os.remove(os.path.join(storage_path, *joke_img.padded_id()))
            request.dbsession.delete(joke_img)
        except Exception:
            pass
        return HTTPOk()
    else:
        raise HTTPNotFound()
