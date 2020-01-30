import json

from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPBadRequest
from pyramid.view import view_config
from sqlalchemy import and_

from toja.config import JOKE_METADATA
from toja.models import Image, Transcription
from toja.session import require_logged_in
from toja.tasks import index_joke
from toja.util import Validator, extract_annotations, extract_text


@view_config(route_name='api.transcriptions.get', renderer='json')
@require_logged_in()
def transcriptions_get(request):
    """GET all the joke :class:`~toja.models.image.Image`. Supports filtering by parent_id and owner_id."""
    transcriptions = request.dbsession.query(Transcription).filter(Transcription.status != 'deleted')
    for key in request.params.keys():
        if key == 'filter[source_id]':
            transcriptions = transcriptions.filter(Transcription.source_id == request.params[key])
        if key == 'filter[owner_id]':
            transcriptions = transcriptions.filter(Transcription.owner_id == request.params[key])
        if key == 'filter[status]':
            transcriptions = transcriptions.filter(Transcription.status == request.params[key])
    return {'data': [transcription.to_jsonapi() for transcription in transcriptions]}


post_transcription_validator = {
    'data': {'type': 'dict',
             'required': True,
             'schema': {'type': {'type': 'string', 'required': True, 'allowed': ['transcriptions']},
                        'attributes': {'type': 'dict',
                                       'required': True,
                                       'schema': {'source_id': {'type': 'integer', 'required': True},
                                                  'text': {'type': 'dict'},
                                                  'status': {'type': 'string', 'required': True}}}}}}
for metadata in JOKE_METADATA:
    if metadata['type'] == 'multichoice':
        post_transcription_validator['data']['schema']['attributes']['schema'][metadata['name']] = \
            {'type': 'list',
             'allowed': [value['name'] for value in metadata['values']]}
    elif metadata['type'] == 'select':
        post_transcription_validator['data']['schema']['attributes']['schema'][metadata['name']] = \
            {'type': 'string',
             'allowed': [value['name'] for value in metadata['values']]}


@view_config(route_name='api.transcriptions.post', renderer='json')
@require_logged_in()
def transcriptions_post(request):
    """POST a new :class:`~toja.models.transcription.Transcription`."""
    if request.current_user.trust != 'full':
        raise HTTPForbidden()
    try:
        params = json.loads(request.body)
    except json.JSONDecodeError:
        raise HTTPBadRequest()
    validator = Validator(post_transcription_validator, purge_unknown=True)
    if validator.validate(params):
        source = request.dbsession.query(Image).filter(and_(Image.id == params['data']['attributes']['source_id'],
                                                            Image.type == 'joke')).first()
        if source:
            transcription = Transcription(source=source,
                                          owner=request.current_user,
                                          text=json.loads(json.dumps(params['data']['attributes']['text']).
                                                          replace('--', '—')),
                                          status='final',
                                          attributes={})
            for metadata in JOKE_METADATA:
                if metadata['type'] == 'extract-single':
                    transcription.attributes[metadata['name']] = \
                        ', '.join([extract_text(node) for node in
                                   extract_annotations(transcription.text, metadata['source']['type'])])
                else:
                    if metadata['name'] in params['data']['attributes']:
                        transcription.attributes[metadata['name']] = params['data']['attributes'][metadata['name']]
            request.dbsession.add(transcription)
            request.dbsession.flush()
            index_joke.send(tid=transcription.id)
            return {'data': transcription.to_jsonapi()}
        else:
            raise HTTPNotFound()
    else:
        raise HTTPBadRequest()
    return {'data': {}}


patch_transcription_validator = {
    'data': {'type': 'dict',
             'required': True,
             'schema': {'type': {'type': 'string', 'required': True, 'allowed': ['transcriptions']},
                        'id': {'type': 'number', 'required': True},
                        'attributes': {'type': 'dict',
                                       'required': True,
                                       'schema': {'source_id': {'type': 'integer', 'required': True},
                                                  'owner_id': {'type': 'integer', 'required': True},
                                                  'text': {'type': 'dict'},
                                                  'status': {'type': 'string', 'required': True}}}}}}
for metadata in JOKE_METADATA:
    if metadata['type'] == 'multichoice':
        patch_transcription_validator['data']['schema']['attributes']['schema'][metadata['name']] = \
            {'type': 'list',
             'allowed': [value['name'] for value in metadata['values']]}
    elif metadata['type'] == 'select':
        patch_transcription_validator['data']['schema']['attributes']['schema'][metadata['name']] = \
            {'type': 'string',
             'allowed': [value['name'] for value in metadata['values']]}


@view_config(route_name='api.transcription.patch', renderer='json')
@require_logged_in()
def transcription_patch(request):
    """PATCH an existing :class:`~toja.models.transcription.Transcription`."""
    if request.current_user.trust != 'full':
        raise HTTPForbidden()
    try:
        params = json.loads(request.body)
    except json.JSONDecodeError:
        raise HTTPBadRequest()
    validator = Validator(patch_transcription_validator, purge_unknown=True)
    if validator.validate(params):
        transcription = request.dbsession.query(Transcription).filter(Transcription.id == request.matchdict['tid']).\
                        first()
        if transcription:
            transcription.text = json.loads(json.dumps(params['data']['attributes']['text']).replace('--', '—'))
            for metadata in JOKE_METADATA:
                if metadata['type'] == 'extract-single':
                    transcription.attributes[metadata['name']] = \
                        ', '.join([extract_text(node) for node in
                                   extract_annotations(transcription.text, metadata['source']['type'])])
                else:
                    if metadata['name'] in params['data']['attributes']:
                        transcription.attributes[metadata['name']] = params['data']['attributes'][metadata['name']]
            request.dbsession.add(transcription)
            index_joke.send(tid=transcription.id)
            return {'data': transcription.to_jsonapi()}
        else:
            raise HTTPNotFound()
    else:
        raise HTTPBadRequest()
    return {'data': {}}
