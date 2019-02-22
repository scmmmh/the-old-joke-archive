from binascii import unhexlify
from pyramid_nacl_session import EncryptedCookieSessionFactory

from .models import User


def get_current_user(request):
    """Get the current user from the database based on the user id set in the request's session.

    :param request: The request used to access the session and database
    :type request: :class:`~pyramid.request.Request`
    """
    if 'user-id' in request.session and hasattr(request, 'dbsession'):
        return request.dbsession.query(User).filter(User.id == request.session['user-id']).first()
    return None


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
