import os
import shutil

from math import ceil
from mimetypes import guess_type
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..permissions import require_permission, check_permission
from ..util import get_config_setting, Validator


@view_config(route_name='contribute.sources', renderer='toja:templates/sources/new.jinja2')
@require_permission('sources.new')
def upload(request):
    """Handles the uploading of new sources."""
    if request.method == 'POST':
        upload_source_schema = {'source': {'type': 'fieldstorage', 'required': True},
                                'license': {'type': 'string', 'required': True, 'allowed': ('on', )}}
        metadata = list(zip(get_config_setting(request, 'app.sources.metadata.fields', target_type='list', default=[]),
                            get_config_setting(request, 'app.sources.metadata.types', target_type='list', default=[])))
        for field, datatype in metadata:
            upload_source_schema[field] = {'type': 'string'}
            if datatype == 'date':
                upload_source_schema[field]['regex'] = '([0-9]{4}-[0-9]{2}-[0-9]{2})?'
        validator = Validator(upload_source_schema)
        storage_path = get_config_setting(request, 'app.images.storage.path')
        if validator.validate(request.params) and storage_path:
            image = Image(owner=request.current_user,
                          type='source',
                          status='processing',
                          attributes={'mimetype': guess_type(request.params['source'].filename)})
            for field, _ in metadata:
                image.attributes[field] = request.params[field]
            request.dbsession.add(image)
            request.dbsession.flush()
            padded_id = image.padded_id()
            os.makedirs(os.path.join(storage_path, *padded_id[0:2]), exist_ok=True)
            with open(os.path.join(storage_path, *padded_id), 'wb') as out_f:
                shutil.copyfileobj(request.params['source'].file, out_f)
            request.session.flash('Your source has been added.', queue='info')
            return HTTPFound(location=request.route_url('user.view', uid=request.current_user.id))
        else:
            return {'errors': validator.errors,
                    'values': request.params}
    return {}


@view_config(route_name='source.index', renderer='toja:templates/sources/index.jinja2')
@require_permission('sources.admin')
def index(request):
    status = request.params.getall('status') if 'status' in request.params else ['processing']
    page = 0
    sources = request.dbsession.query(Image).filter(and_(Image.type == 'source',
                                                         Image.status.in_(status)))
    total = sources.count()
    sources = sources.offset(page * 10).limit(page * 10 + 10)
    return {'sources': sources,
            'status': status,
            'pagination': {'start': max(0, page - 2),
                           'current': page,
                           'end': min(ceil(total / 10), page + 2),
                           'total': total}}


@view_config(route_name='source.view', renderer='toja:templates/sources/view.jinja2')
@require_permission('sources.admin or @view image :sid')
def view(request):
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source',
                                                        Image.status != 'deleted')).first()
    if source:
        return {'source': source}
    else:
        raise HTTPNotFound()


@view_config(route_name='source.edit', renderer='toja:templates/sources/edit.jinja2')
@require_permission('sources.admin or @edit image :sid')
def edit(request):
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source'))
    if not check_permission(request, request.current_user, 'sources.admin'):
        source = source.filter(Image.status == 'processing')
    source = source.first()
    if source:
        if request.method == 'POST':
            edit_source_schema = {}
            if check_permission(request, request.current_user, 'sources.admin'):
                edit_source_schema['status'] = {'type': 'string',
                                                'required': True,
                                                'allowed': ['processing', 'completed', 'deleted']}
            metadata = list(zip(get_config_setting(request, 'app.sources.metadata.fields', target_type='list',
                                                   default=[]),
                                get_config_setting(request, 'app.sources.metadata.types', target_type='list',
                                                   default=[])))
            for field, datatype in metadata:
                edit_source_schema[field] = {'type': 'string'}
                if datatype == 'date':
                    edit_source_schema[field]['regex'] = '([0-9]{4}-[0-9]{2}-[0-9]{2})?'
            validator = Validator(edit_source_schema)
            if validator.validate(request.params):
                for name, _ in metadata:
                    source.attributes[name] = request.params[name]
                if check_permission(request, request.current_user, 'sources.admin'):
                    source.status = request.params['status']
                if check_permission(request, request.current_user, 'sources.admin'):
                    return HTTPFound(request.route_url('source.index'))
                else:
                    return HTTPFound(request.route_url('source.view', sid=source.id))
            else:
                return {'source': source,
                        'errors': validator.errors,
                        'values': request.params}
        return {'source': source}
    else:
        raise HTTPNotFound()


@view_config(route_name='source.delete')
@require_permission('sources.admin or @delete image :sid')
def delete(request):
    source = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                        Image.type == 'source',
                                                        Image.status != 'deleted')).first()
    if source:
        if request.method == 'POST':
            source.status = 'deleted'
            if check_permission(request, request.current_user, 'sources.admin'):
                return HTTPFound(request.route_url('source.index'))
            else:
                return HTTPFound(request.route_url('user.view', uid=request.current_user.id))
        return {'source': source}
    else:
        raise HTTPNotFound()
