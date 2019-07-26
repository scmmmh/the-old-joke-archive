import json
import os

from base64 import b64encode
from PIL import Image as PILImage
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest, HTTPNoContent
from pyramid.view import view_config
from sqlalchemy import and_

from toja.models import Image
from toja.session import require_logged_in
from toja.util import date_to_json, Validator, get_config_setting


def to_jsonapi(request, joke):
    """Render a joke :class:`~toja.models.image.Image`."""
    storage_path = get_config_setting(request, 'app.images.storage.path')
    with open(os.path.join(storage_path, *joke.padded_id()), 'rb') as in_f:
        raw_data = b64encode(in_f.read())
    attrs = {'status': joke.status,
             'created': date_to_json(joke.created),
             'updated': date_to_json(joke.updated) if joke.updated else None,
             'raw': 'data:{0};base64,{1}'.format(joke.attributes['mimetype'], raw_data.decode('utf8')),
             'parent_id': joke.parent_id}
    attrs.update(joke.attributes)
    return {'type': 'jokes',
            'id': joke.id,
            'attributes': attrs}


@view_config(route_name='api.jokes.get', renderer='json')
@require_logged_in()
def jokes_get(request):
    """GET all the joke :class:`~toja.models.image.Image` for a source :class:`~toja.models.image.Image`
    (identified by the parameter ``sid``)."""
    jokes = request.dbsession.query(Image).filter(and_(Image.parent_id == request.matchdict['sid'],
                                                       Image.status != 'deleted'))
    return {'data': [to_jsonapi(request, joke) for joke in jokes]}


post_joke_validator = {
    'data': {'type': 'dict',
             'required': True,
             'schema': {'type': {'type': 'string', 'required': True, 'allowed': ['jokes']},
                        'attributes': {'type': 'dict',
                                       'required': True,
                                       'schema': {'bbox': {'type': 'dict',
                                                           'required': True,
                                                           'schema': {'left': {'type': 'float', 'required': True},
                                                                      'top': {'type': 'float', 'required': True},
                                                                      'width': {'type': 'float', 'required': True},
                                                                      'height': {'type': 'float', 'required': True}}},
                                                  'parent_id': {'type': 'integer', 'required': True}}}}}}


@view_config(route_name='api.jokes.post', renderer='json')
@require_logged_in()
def jokes_post(request):
    """Add a new joke :class:`~toja.models.image.Image` to the source :class:`~toja.models.image.Image`
    (identified by the parameter ``sid``)."""
    if request.current_user.trust != 'full':
        raise HTTPForbidden()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if storage_path is None:
        raise HTTPNotFound()
    try:
        params = json.loads(request.body)
        validator = Validator(post_joke_validator)
        if validator.validate(params):
            source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                                Image.status == 'processing')).first()
            if source is not None:
                params['data']['attributes']['bbox']['left'] = int(params['data']['attributes']['bbox']['left'])
                params['data']['attributes']['bbox']['top'] = int(params['data']['attributes']['bbox']['top'])
                params['data']['attributes']['bbox']['width'] = int(params['data']['attributes']['bbox']['width'])
                params['data']['attributes']['bbox']['height'] = int(params['data']['attributes']['bbox']['height'])
                source_img = PILImage.open(os.path.join(storage_path, *source.padded_id()))
                joke = Image(owner=request.current_user,
                             parent=source,
                             attributes={'mimetype': 'image/jpeg',
                                         'bbox': params['data']['attributes']['bbox']},
                             type='joke',
                             status='confirmed' if request.current_user.trust == 'full' else 'new')
                request.dbsession.add(joke)
                request.dbsession.flush()
                joke_img = source_img.crop((params['data']['attributes']['bbox']['left'],
                                            params['data']['attributes']['bbox']['top'],
                                            params['data']['attributes']['bbox']['left'] +
                                            params['data']['attributes']['bbox']['width'],
                                            params['data']['attributes']['bbox']['top'] +
                                            params['data']['attributes']['bbox']['height']))
                os.makedirs(os.path.join(storage_path, *joke.padded_id()[0:2]), exist_ok=True)
                joke_img.save(os.path.join(storage_path, *joke.padded_id()), format='jpeg')
                return {'data': to_jsonapi(request, joke)}
            else:
                raise HTTPBadRequest()
        else:
            raise HTTPBadRequest()
    except json.JSONDecodeError:
        raise HTTPBadRequest()


put_joke_validator = {
    'data': {'type': 'dict',
             'required': True,
             'schema': {'type': {'type': 'string', 'required': True, 'allowed': ['jokes']},
                        'id': {'type': 'integer'},
                        'attributes': {'type': 'dict',
                                       'required': True,
                                       'schema': {'bbox': {'type': 'dict',
                                                           'required': True,
                                                           'schema': {'left': {'type': 'float', 'required': True},
                                                                      'top': {'type': 'float', 'required': True},
                                                                      'width': {'type': 'float', 'required': True},
                                                                      'height': {'type': 'float', 'required': True}}},
                                                  'parent_id': {'type': 'integer', 'required': True},
                                                  'created': {'type': 'string'},
                                                  'updated': {'type': 'string', 'nullable': True},
                                                  'mimetype': {'type': 'string'},
                                                  'status': {'type': 'string'},
                                                  'raw': {'type': 'string'}}}}}}


@view_config(route_name='api.joke.put', renderer='json')
@require_logged_in()
def joke_put(request):
    """Updates a single joke :class:`~toja.models.image.Image` (identified by the parameter ``jid``) inside a
    source :class:`~toja.models.image.Image` (identified by the parameter ``sid``)."""
    if request.current_user.trust != 'full':
        raise HTTPForbidden()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if storage_path is None:
        raise HTTPNotFound()
    try:
        params = json.loads(request.body)
        validator = Validator(put_joke_validator)
        if validator.validate(params):
            source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                                Image.status == 'processing')).first()
            joke = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                              Image.parent_id == request.matchdict['sid'])).first()
            if source is None or joke is None:
                raise HTTPNotFound()
            params['data']['attributes']['bbox']['left'] = int(params['data']['attributes']['bbox']['left'])
            params['data']['attributes']['bbox']['top'] = int(params['data']['attributes']['bbox']['top'])
            params['data']['attributes']['bbox']['width'] = int(params['data']['attributes']['bbox']['width'])
            params['data']['attributes']['bbox']['height'] = int(params['data']['attributes']['bbox']['height'])
            source_img = PILImage.open(os.path.join(storage_path, *source.padded_id()))
            joke_img = source_img.crop((params['data']['attributes']['bbox']['left'],
                                        params['data']['attributes']['bbox']['top'],
                                        params['data']['attributes']['bbox']['left'] +
                                        params['data']['attributes']['bbox']['width'],
                                        params['data']['attributes']['bbox']['top'] +
                                        params['data']['attributes']['bbox']['height']))
            os.makedirs(os.path.join(storage_path, *joke.padded_id()[0:2]), exist_ok=True)
            joke_img.save(os.path.join(storage_path, *joke.padded_id()), format='jpeg')
            joke.attributes['bbox'] = params['data']['attributes']['bbox']
            request.dbsession.add(joke)
            """if source is not None:
                joke = Image(owner=request.current_user,
                             parent=source,
                             attributes={'mimetype': 'image/jpeg',
                                         'bbox': params['data']['attributes']['bbox']},
                             type='joke',
                             status='confirmed' if request.current_user.trust == 'full' else 'new')
                request.dbsession.add(joke)
                request.dbsession.flush()
                print(params['data']['attributes']['bbox'])
                joke_img = source_img.crop((params['data']['attributes']['bbox']['left'],
                                            params['data']['attributes']['bbox']['top'],
                                            params['data']['attributes']['bbox']['left'] +
                                            params['data']['attributes']['bbox']['width'],
                                            params['data']['attributes']['bbox']['top'] +
                                            params['data']['attributes']['bbox']['height']))
                os.makedirs(os.path.join(storage_path, *joke.padded_id()[0:2]), exist_ok=True)
                joke_img.save(os.path.join(storage_path, *joke.padded_id()), format='jpeg')
                return {'data': to_jsonapi(request, joke)}"""
            return {'data': to_jsonapi(request, joke)}
        else:
            print(validator.errors)
            raise HTTPBadRequest()
    except json.JSONDecodeError:
        raise HTTPBadRequest()


@view_config(route_name='api.joke.delete', renderer='json')
@require_logged_in()
def joke_delete(request):
    """Deletes a single joke :class:`~toja.models.image.Image` (identified by the parameter ``jid``) inside a
    source :class:`~toja.models.image.Image` (identified by the parameter ``sid``)."""
    if request.current_user.trust != 'full':
        raise HTTPForbidden()
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.status == 'processing')).first()
    joke = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['jid'],
                                                      Image.parent_id == request.matchdict['sid'])).first()
    if source is None or joke is None:
        raise HTTPNotFound()
    joke.status = 'deleted'
    request.dbsession.add(joke)
    return HTTPNoContent()
