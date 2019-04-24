import json
import os

from PIL import Image as PILImage
from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPOk
from pyramid.view import view_config
from random import sample, choice
from sqlalchemy import and_, or_, func

from ..models import Image, Review
from ..util import get_config_setting
from ..session import require_logged_in
from ..tasks import ocr_single_image


@view_config(route_name='crowdsourcing', renderer='toja:templates/crowdsourcing/index.jinja2')
def crowdsourcing(request):
    """Handles the crowdsourcing overview."""
    # Sources to extract from are those with the status processing.
    sources_count = request.dbsession.query(Image).filter(and_(Image.type == 'source',
                                                               Image.status == 'processing')).count()
    # Verifiable jokes are those that are new and are neither uploaded or reviewed by the same user.
    verify_jokes_count = request.dbsession.query(func.count(Image.id)).outerjoin(Image.reviews).\
        filter(and_(Image.type == 'joke',
                    Image.status == 'new',
                    Image.owner_id != (request.current_user.id if
                                       request.current_user else
                                       -1),
                    or_(Review.owner_id == None,
                        Review.owner_id != (request.current_user.id if
                                            request.current_user else
                                            -1)))).first()[0]  # noqa: E711
    return {'counts': {'sources': sources_count,
                       'verify_jokes': verify_jokes_count}}


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
                         status='confirmed' if request.current_user.trust == 'full' else 'new')
        request.dbsession.add(joke_img)
        request.dbsession.flush()
        part_img = source_img.crop((int(body['data']['attributes']['bbox']['left']),
                                    int(body['data']['attributes']['bbox']['top']),
                                    int(body['data']['attributes']['bbox']['left']) +
                                    int(body['data']['attributes']['bbox']['width']),
                                    int(body['data']['attributes']['bbox']['top']) +
                                    int(body['data']['attributes']['bbox']['height'])))
        part_img.save(os.path.join(storage_path, *joke_img.padded_id()), format='jpeg')
        ocr_single_image.apply_async(args=(joke_img.id,), countdown=30)
        return {'data': {'types': 'images',
                         'id': joke_img.id,
                         'attributes': joke_img.attributes}}
    else:
        raise HTTPNotFound()


@view_config(route_name='crowdsourcing.identify.update', renderer='json')
@require_logged_in()
def update_joke(request):
    """Update an extracted joke."""
    # TODO: Need to check that the image has not been processed furhter before allowing edit/delete
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
        joke_img.status = 'confirmed' if request.current_user.trust == 'full' else 'new'
        request.dbsession.add(joke_img)
        request.dbsession.flush()
        part_img = source_img.crop((int(body['data']['attributes']['bbox']['left']),
                                    int(body['data']['attributes']['bbox']['top']),
                                    int(body['data']['attributes']['bbox']['left']) +
                                    int(body['data']['attributes']['bbox']['width']),
                                    int(body['data']['attributes']['bbox']['top']) +
                                    int(body['data']['attributes']['bbox']['height'])))
        part_img.save(os.path.join(storage_path, *joke_img.padded_id()), format='jpeg')
        ocr_single_image.apply_async(args=(joke_img.id,), countdown=30)
        return {'data': {'types': 'images',
                         'id': joke_img.id,
                         'attributes': joke_img.attributes}}
    else:
        raise HTTPNotFound()


@view_config(route_name='crowdsourcing.identify.delete', renderer='json')
@require_logged_in()
def delete_joke(request):
    """Update an extracted joke."""
    # TODO: Need to check that the image has not been processed furhter before allowing edit/delete
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


@view_config(route_name='crowdsourcing.verify_jokes', renderer='toja:templates/crowdsourcing/verify_jokes.jinja2')
@require_logged_in()
def verify_jokes(request):
    """Display an extracted joke for verification."""
    joke_ids = [i.id for i in request.dbsession.query(Image.id).outerjoin(Image.reviews).
                filter(and_(Image.type == 'joke',
                            Image.status == 'new',
                            Image.owner_id != request.current_user.id,
                            or_(Review.owner_id == None,
                                Review.owner_id != request.current_user.id)))]  # noqa: E711
    if joke_ids:
        joke = request.dbsession.query(Image).filter(Image.id == choice(joke_ids)).first()
        return {'joke': joke}
    else:
        request.session.flash('Thank you for your help. There are currently no outstanding jokes for you to check.',
                              'info')
        raise HTTPFound(request.route_url('crowdsourcing'))


@view_config(route_name='crowdsourcing.verify_joke')
@require_logged_in()
def verify_joke(request):
    """Handle the verification of a single extracted joke."""
    joke = request.dbsession.query(Image).outerjoin(Image.reviews).\
        filter(and_(Image.id == request.matchdict['jid'],
                    Image.type == 'joke',
                    Image.status == 'new',
                    Image.owner_id != request.current_user.id,
                    or_(Review.owner_id == None,
                        Review.owner_id != request.current_user.id))).first()  # noqa: E711
    if joke and 'status' in request.params and request.params['status'] in ['clean', 'not-clean']:
        review = Review(owner=request.current_user,
                        attributes={'review': request.params['status']})
        joke.reviews.append(review)
    request.session.flash('Thank you for your help.', 'info')
    return HTTPFound(request.route_url('crowdsourcing.verify_jokes'))
