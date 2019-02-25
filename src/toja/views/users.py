from copy import deepcopy
from email_validator import validate_email, EmailNotValidError
from hashlib import sha512
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
try:
    from secrets import token_hex
except:
    from .p35_secrets import token_hex
from sqlalchemy import and_

from ..models import User
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
                            'empty': False}}


@view_config(route_name='users.register', renderer='../templates/users/register.jinja2')
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
        validator = Validator(schema)
        if validator.validate(request.params):
            user = User(email=request.params['email'],
                        name=request.params['name'],
                        salt=None,
                        password=None,
                        status='new',
                        trust='',
                        groups=[],
                        permissions=[],
                        attributes={'validation_token': token_hex(32)})
            if request.dbsession.query(User).count() == 0:
                user.groups.append('admin')
                user.trust = 'full'
            request.dbsession.add(user)
            request.session.flash('You have registered. You should shortly receive a confirmation e-mail.', 'info')
            send_email(request, user.email, get_config_setting(request, 'app.email.sender', default='toja@example.com'),
                'Confirm your registration with The Old Joke Archive', '''Dear %(name)s,

Welcome to The Old Joke Archive. We just need to confirm your e-mail address.
Please click on the following link or copy it into your browser:

%(url)s

Thank you,
The Old Joke Archive
''' % {'name': user.name, 'url': request.route_url('users.confirm',
                                               email=user.email,
                                               token=user.attributes['validation_token'])})
            return HTTPFound(location=request.route_url('root'))
        else:
            return {'errors': validator.errors,
                    'values': request.params}
    return {'errors': {}}


confirmation_schema = {'password': {'type': 'string', 'empty': False},
                       'confirm_password': {'type': 'string', 'empty': False, 'matches': 'password'}}


@view_config(route_name='users.confirm', renderer='../templates/users/confirm.jinja2')
def confirm(request):
    """Handles the user confirmation and setting a new password. Confirmed users are automatically logged in."""
    user = request.dbsession.query(User).filter(and_(User.email == request.matchdict['email'],
                                                     User.status == 'new')).first()
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
                user.status = 'confirmed'
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
        return {}


login_schema = {'email': {'type': 'string', 'empty': False, 'validator': valid_email},
                'password': {'type': 'string', 'empty': False}}


@view_config(route_name='users.login', renderer='../templates/users/login.jinja2')
def login(request):
    """Handle logging the user in."""
    if request.method == 'POST':
        validator = Validator(login_schema)
        if validator.validate(request.params):
            user = request.dbsession.query(User).filter(User.email == request.params['email']).first()
            if user:
                hash = sha512()
                hash.update(user.salt.encode('utf-8'))
                hash.update(b'$$')
                hash.update(request.params['password'].encode('utf-8'))
                if user.password == hash.hexdigest():
                    request.session['user-id'] = user.id
                    return HTTPFound(location=request.route_url('root'))
            return {'errors': {'email': ['Either there is no user with this e-mail address or the password is incorrect.'],
                               'password': ['Either there is no user with this e-mail address or the password is incorrect.']},
                    'values': request.params}
        else:
            return {'errors': validator.errors, 'values': request.params}
    return {}


@view_config(route_name='users.logout', renderer='../templates/users/logout.jinja2')
def logout(request):
    """Handle logging the user out."""
    if request.method == 'POST':
        request.session.clear()
        return HTTPFound(location=request.route_url('root'))
    return {}
