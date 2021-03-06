from copy import deepcopy
from email_validator import validate_email, EmailNotValidError
from hashlib import sha512
from math import ceil
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config
from random import sample, choice
from secrets import token_hex
from sqlalchemy import and_

from ..models import User
from ..permissions import require_permission, check_permission, PERMISSIONS, GROUPS
from ..routes import decode_route
from ..util import get_config_setting, send_email, Validator


def valid_email(field, value, error):
    """Validates that the ``value`` in ``field`` is a valid e-mail address.

    :param field: The field being validated
    :type field: str
    :param value: The field value to validate
    :param error: Callback to set the error message, if the ``value`` is not valid
    """
    try:
        validate_email(value, check_deliverability=False)
    except EmailNotValidError as e:
        error(field, str(e))


register_schema = {'email': {'type': 'string',
                             'required': True,
                             'validator': [valid_email]},
                   'name': {'type': 'string',
                            'required': True,
                            'empty': False},
                   'icon': {'type': 'string',
                            'required': True,
                            'allowed': []}}
VALIDATION_ICONS = [('pencil', 'pencil'), ('anvil', 'anvil'), ('tree', 'tree'), ('water', 'water'), ('cloud', 'cloud'),
                    ('flower', 'flower'), ('elephant', 'elephant'), ('airplane', 'plane'),
                    ('airballoon', 'hot air balloon'), ('bus', 'bus'), ('fingerprint', 'fingerprint'),
                    ('phone', 'phone'), ('star', 'star'), ('watch', 'watch'), ('food-apple', 'apple')]


@view_config(route_name='user.register', renderer='toja:templates/users/register.jinja2')
def register(request):
    """Handles the registration of new users."""
    if request.method == 'POST':
        def nonexistant_email(field, value, error):
            """Checks that the ``value`` in ``field`` is not already registered.
            """
            if request.dbsession.query(User).filter(User.email == value).first():
                error(field, 'This e-mail address is already registered.')

        schema = deepcopy(register_schema)
        schema['email']['validator'].append(nonexistant_email)
        if 'verification_id' in request.session:
            schema['icon']['allowed'].append(request.session['verification_id'])
        validator = Validator(schema)
        if validator.validate(request.params):
            user = User(email=request.params['email'].lower(),
                        salt=None,
                        password=None,
                        status='new',
                        trust='low',
                        groups=[],
                        permissions=[],
                        attributes={'validation_token': token_hex(32),
                                    'name': request.params['name']})
            if request.dbsession.query(User).count() == 0:
                user.groups.append('admin')
                user.trust = 'full'
            request.dbsession.add(user)
            request.session.flash('You have registered. You should shortly receive a confirmation e-mail.', 'info')
            send_email(request, user.email, get_config_setting(request,
                                                               'app.email.sender',
                                                               default='admin@the-old-joke-archive.org'),
                       'Confirm your registration with The Old Joke Archive', '''Dear %(name)s,

Welcome to The Old Joke Archive. We just need to confirm your e-mail address.
Please click on the following link or copy it into your browser:

%(url)s

Thank you,
The Old Joke Archive
''' % {'name': user.attributes['name'], 'url': request.route_url('user.confirm',
                                                                 email=user.email,
                                                                 token=user.attributes['validation_token'])})
            return HTTPFound(location=request.route_url('root'))
        else:
            verification_icons = list(enumerate(sample(VALIDATION_ICONS, 7)))
            selected_icon = choice(verification_icons[1:])
            request.session['verification_id'] = str(selected_icon[0])
            return {'errors': validator.errors,
                    'values': request.params,
                    'verification_icons': verification_icons,
                    'selected_icon': selected_icon[1]}
    verification_icons = list(enumerate(sample(VALIDATION_ICONS, 7)))
    selected_icon = choice(verification_icons[1:])
    request.session['verification_id'] = str(selected_icon[0])
    return {'errors': {},
            'verification_icons': verification_icons,
            'selected_icon': selected_icon[1]}


confirmation_schema = {'password': {'type': 'string', 'empty': False},
                       'confirm_password': {'type': 'string', 'empty': False, 'matches': 'password'}}


@view_config(route_name='user.confirm', renderer='toja:templates/users/confirm.jinja2')
def confirm(request):
    """Handles the user confirmation and setting a new password. Users are automatically logged in."""
    user = request.dbsession.query(User).filter(User.email == request.matchdict['email']).first()
    if user and 'validation_token' in user.attributes and \
            user.attributes['validation_token'] == request.matchdict['token']:
        if request.method == 'POST':
            validator = Validator(confirmation_schema)
            if validator.validate(request.params):
                user.salt = token_hex(32)
                hash = sha512()
                hash.update(user.salt.encode('utf-8'))
                hash.update(b'$$')
                hash.update(request.params['password'].encode('utf-8'))
                user.password = hash.hexdigest()
                user.status = 'active'
                del user.attributes['validation_token']
                request.session['user-id'] = user.id
                request.session.flash('You have updated your password.', 'info')
                return HTTPFound(location=request.route_url('root'))
            else:
                return {'user': user,
                        'errors': validator.errors,
                        'values': request.params}
        return {'user': user}
    else:
        request.session.flash('Unfortunately that validation token is not valid for that e-mail address.', queue='info')
        return HTTPFound(location=request.route_url('root'))


login_schema = {'email': {'type': 'string', 'empty': False, 'validator': valid_email},
                'password': {'type': 'string', 'empty': False},
                'redirect': {'type': 'string'}}


@view_config(route_name='user.login', renderer='toja:templates/users/login.jinja2')
def login(request):
    """Handle logging the user in."""
    if request.method == 'POST':
        validator = Validator(login_schema)
        if validator.validate(request.params):
            user = request.dbsession.query(User).filter(and_(User.email == request.params['email'].lower(),
                                                             User.status == 'active')).first()
            if user:
                hash = sha512()
                hash.update(user.salt.encode('utf-8'))
                hash.update(b'$$')
                hash.update(request.params['password'].encode('utf-8'))
                if user.password == hash.hexdigest():
                    request.session['user-id'] = user.id
                    return HTTPFound(location=decode_route(request, 'user.view', {'uid': user.id}))
            return {'errors': {'email': ['Either there is no user with this e-mail address ' +
                                         'or the password is incorrect.'],
                               'password': ['Either there is no user with this e-mail address ' +
                                            'or the password is incorrect.']},
                    'values': request.params}
        else:
            return {'errors': validator.errors, 'values': request.params}
    return {}


forgotten_password_schema = {'email': {'type': 'string', 'empty': False, 'validator': valid_email}}


@view_config(route_name='user.forgotten_password', renderer='toja:templates/users/forgotten_password.jinja2')
def forgotten_password(request):
    """Handle sending a link for a forgotten password."""
    if request.method == 'POST':
        validator = Validator(login_schema)
        if validator.validate(request.params):
            user = request.dbsession.query(User).filter(and_(User.email == request.params['email'].lower(),
                                                             User.status == 'active')).first()
            if user:
                user.attributes['validation_token'] = token_hex(32)
                request.dbsession.add(user)
                send_email(request, user.email, get_config_setting(request,
                                                                   'app.email.sender',
                                                                   default='admin@the-old-joke-archive.org'),
                           'Reset your password at The Old Joke Archive', '''Dear %(name)s,

You have asked to have your password reset. To do so, plese click on the following link or copy it into your browser:

%(url)s

If you did not request this, then probably somebody is blindly trying e-mail addresses. As long as this person has
no access to your e-mail account, they will neither be able to reset your password, nor to find out that this e-mail
address works.

Thank you,
The Old Joke Archive
''' % {'name': user.attributes['name'], 'url': request.route_url('user.confirm',
                                                                 email=user.email,
                                                                 token=user.attributes['validation_token'])})
            request.session.flash('An email with a password reset link has been sent to the email address.', 'info')
            return HTTPFound(request.route_url('root'))
        else:
            return {'errors': validator.errors, 'values': request.params}
    return {}


@view_config(route_name='user.logout', renderer='toja:templates/users/logout.jinja2')
def logout(request):
    """Handle logging the user out."""
    if request.method == 'POST':
        request.session.clear()
        return HTTPFound(location=request.route_url('root'))
    return {}


@view_config(route_name='user.index', renderer='toja:templates/users/index.jinja2')
@require_permission('users.admin')
def index(request):
    """Handle displaying the list of users. Supports filtering by email address and status."""
    status = request.params.getall('status') if 'status' in request.params else ['active']
    page = 0
    users = request.dbsession.query(User).filter(User.status.in_(status))
    if 'q' in request.params and request.params['q'].strip():
        users = users.filter(User.email.like('%%%s%%' % request.params['q'].strip().lower()))
    total = users.count()
    users = users.offset(page * 10).limit(page * 10 + 10)
    return {'users': users,
            'status': status,
            'pagination': {'start': max(0, page - 2),
                           'current': page,
                           'end': min(ceil(total / 10), page + 2),
                           'total': total}}


@view_config(route_name='user.view', renderer='toja:templates/users/view.jinja2')
@require_permission('users.admin or @view user :uid')
def view(request):
    """Handle displaying the user's profile."""
    user = request.dbsession.query(User).filter(User.id == request.matchdict['uid']).first()
    if user:
        return {'user': user}
    else:
        raise HTTPNotFound()


@view_config(route_name='user.edit', renderer='toja:templates/users/edit.jinja2')
@require_permission('users.admin or @edit user :uid')
def edit(request):
    """Handle editing users, both for admins and the users themselves."""
    user = request.dbsession.query(User).filter(User.id == request.matchdict['uid']).first()
    if user:
        if request.method == 'POST':
            edit_schema = {'email': {'type': 'string', 'required': True, 'validator': [valid_email]},
                           'name': {'type': 'string', 'required': True, 'empty': False},
                           'password': {'type': 'string', 'empty': True},
                           'confirm_password': {'type': 'string', 'empty': True, 'matches': 'password'}}
            if check_permission(request, request.current_user, 'users.admin'):
                edit_schema['status'] = {'type': 'string', 'required': True,
                                         'allowed': ['new', 'active', 'deleted', 'blocked']}
                edit_schema['trust'] = {'type': 'string', 'required': True,
                                        'allowed': ['low', 'medium', 'high', 'full']}
                edit_schema['group'] = {'type': 'string', 'allowed': list(GROUPS.keys())}
                edit_schema['permission'] = {'type': 'string', 'allowed': list(PERMISSIONS.keys())}
            validator = Validator(edit_schema)
            if validator.validate(request.params):
                user.attributes['name'] = request.params['name']
                user.email = request.params['email'].lower()
                if request.params['password']:
                    user.salt = token_hex(32)
                    hash = sha512()
                    hash.update(user.salt.encode('utf-8'))
                    hash.update(b'$$')
                    hash.update(request.params['password'].encode('utf-8'))
                    user.password = hash.hexdigest()
                if check_permission(request, request.current_user, 'users.admin'):
                    user.status = request.params['status']
                    user.trust = request.params['trust']
                    user.groups = request.params.getall('group')
                    user.permissions = request.params.getall('permission')
                if check_permission(request, request.current_user, 'users.admin'):
                    return HTTPFound(request.route_url('user.index'))
                else:
                    return HTTPFound(request.route_url('user.view', uid=user.id))
            else:
                return {'user': user,
                        'groups': GROUPS.keys(),
                        'permissions': PERMISSIONS,
                        'errors': validator.errors,
                        'values': request.params}
        else:
            return {'user': user,
                    'groups': GROUPS.keys(),
                    'permissions': PERMISSIONS}
    else:
        raise HTTPNotFound()


@view_config(route_name='user.delete')
@require_permission('users.admin or @delete user :uid')
def delete(request):
    """Handle deleting users, both for admins and the users themselves."""
    user = request.dbsession.query(User).filter(User.id == request.matchdict['uid']).first()
    if user:
        if user.status == 'new':
            request.dbsession.delete(user)
        else:
            user.attributes['name'] = 'Deleted User'
            user.email = 'deleted-{0}@the-old-joke-archive.org'.format(user.id)
            user.salt = ''
            user.password = ''
            user.status = 'deleted'
        if check_permission(request, request.current_user, 'users.admin'):
            return HTTPFound(request.route_url('user.index'))
        else:
            return HTTPFound(request.route_url('root'))
    else:
        raise HTTPNotFound()
