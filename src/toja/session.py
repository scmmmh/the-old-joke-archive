from binascii import unhexlify
from decorator import decorator
from pyramid.httpexceptions import HTTPForbidden
from pyramid_nacl_session import EncryptedCookieSessionFactory
from sqlalchemy import and_

from .models import User


def get_current_user(request):
    """Get the current user from the database based on the user id set in the request's session.

    :param request: The request used to access the session and database
    :type request: :class:`~pyramid.request.Request`
    """
    if 'user-id' in request.session and hasattr(request, 'dbsession'):
        return request.dbsession.query(User).filter(and_(User.id == request.session['user-id'],
                                                         User.status == 'active')).first()
    return None


def require_logged_in():
    """Pyramid decorator to check the request is logged in."""
    def handler(f, *args, **kwargs):
        if args[0].current_user is not None:
            return f(*args, **kwargs)
        else:
            raise HTTPForbidden()
    return decorator(handler)


def logged_in(request):
    """Jinja2 filter that checks if the current user is logged in."""
    return request.current_user is not None


def includeme(config):
    """Setup the session handling in the configuration."""
    secret = unhexlify(config.get_settings()['app.session_secret'].strip())
    factory = EncryptedCookieSessionFactory(secret, cookie_name='toja')
    config.set_session_factory(factory)

    config.add_request_method(
        get_current_user,
        'current_user',
        reify=True
    )

    config.get_jinja2_environment().filters['logged_in'] = logged_in
