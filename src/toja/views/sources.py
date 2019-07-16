import os
import shutil

from mimetypes import guess_type
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from ..models import Image
from ..permissions import require_permission
from ..util import get_config_setting, Validator


@view_config(route_name='contribute.sources', renderer='toja:templates/sources/new.jinja2')
@require_permission('sources.new')
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
