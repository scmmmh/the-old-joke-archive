import os
import shutil

from mimetypes import guess_type
from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPMethodNotAllowed
from pyramid.response import FileResponse
from pyramid.view import view_config
from sqlalchemy import and_

from ..models import Image
from ..permissions import require_permission
from ..util import get_config_setting, Validator


@view_config(route_name='sources.upload', renderer='toja:templates/sources/upload.jinja2')
@require_permission('sources.upload')
def upload(request):
    """Handles the uploading of new sources."""
    if request.method == 'POST':
        upload_source_schema = {'source': {'type': 'fieldstorage', 'required': True}}
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
                          status='new',
                          attributes={'mimetype': guess_type(request.params['source'].filename)})
            for field, _ in metadata:
                image.attributes[field] = request.params[field]
            request.dbsession.add(image)
            request.dbsession.flush()
            padded_id = '%09i' % image.id
            padded_id = (padded_id[0:3], padded_id[3:6], padded_id[6:9])
            os.makedirs(os.path.join(storage_path, *padded_id[0:2]), exist_ok=True)
            with open(os.path.join(storage_path, *padded_id), 'wb') as out_f:
                shutil.copyfileobj(request.params['source'].file, out_f)
            return HTTPFound(location=request.route_url('sources.list'))
        else:
            return {'errors': validator.errors,
                    'values': request.params}
    return {}


@view_config(route_name='sources.list', renderer='toja:templates/sources/list.jinja2')
@require_permission('sources.list')
def index(request):
    """Handles the display of all sources."""
    images = request.dbsession.query(Image).filter(Image.type == 'source')
    metadata = list(zip(get_config_setting(request, 'app.sources.metadata.fields', target_type='list', default=[]),
                        get_config_setting(request, 'app.sources.metadata.types', target_type='list', default=[]),
                        get_config_setting(request, 'app.sources.metadata.labels', target_type='list', default=[])))
    return {'images': images,
            'metadata': metadata}


@view_config(route_name='sources.view.image')
def image(request):
    """Send the image data for a single source image."""
    image = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                       Image.type == 'source')).first()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if image and storage_path:
        padded_id = '%09i' % image.id
        padded_id = (padded_id[0:3], padded_id[3:6], padded_id[6:9])
        path = os.path.join(storage_path, *padded_id)
        return FileResponse(path, request=request, content_type=image.attributes['mimetype'][0])
    else:
        raise HTTPNotFound()


@view_config(route_name='sources.edit.attribute')
@require_permission('sources.edit')
def edit_attribute(request):
    """Update a single attribute on a source image."""
    if request.method == 'POST':
        image = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                           Image.type == 'source')).first()
        fields = get_config_setting(request, 'app.sources.metadata.fields', target_type='list', default=[])
        if image and request.matchdict['attribute'] in fields:
            edit_schema = {request.matchdict['attribute']: {'type': 'string'}}
            validator = Validator(edit_schema)
            if validator.validate(request.params):
                image.attributes[request.matchdict['attribute']] = request.params[request.matchdict['attribute']]
            return HTTPFound(location=request.route_url('sources.list'))
        else:
            raise HTTPNotFound()
    else:
        raise HTTPMethodNotAllowed()


@view_config(route_name='sources.delete')
@require_permission('sources.delete')
def delete(request):
    """Delete a single source image."""
    image = request.dbsession.query(Image).filter(and_(Image.id == request.matchdict['sid'],
                                                       Image.type == 'source')).first()
    storage_path = get_config_setting(request, 'app.images.storage.path')
    if image and storage_path:
        padded_id = '%09i' % image.id
        padded_id = (padded_id[0:3], padded_id[3:6], padded_id[6:9])
        path = os.path.join(storage_path, *padded_id)
        try:
            os.remove(path)
            request.dbsession.delete(image)
        except Exception:
            pass
        return HTTPFound(request.route_url('sources.list'))
    else:
        raise HTTPNotFound()
