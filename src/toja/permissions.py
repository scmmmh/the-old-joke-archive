from decorator import decorator
from pyramid.httpexceptions import HTTPForbidden, HTTPFound

from .routes import encode_route


PERMISSIONS = ['admin.view',
               'users.list',
               'users.edit',
               'users.delete',
               'sources.list',
               'sources.upload',
               'sources.edit',
               'sources.delete']
GROUPS = {'admin': ['admin.view', 'users.list', 'users.edit', 'users.delete', 'sources.list', 'sources.upload',
                    'sources.edit', 'sources.delete']}
PERMISSIONS_GROUPS = dict([permission, group] for group, permissions in GROUPS.items() for permission in permissions)


def has_permission(user, permission):
    """Checks whether the given ``user`` has the given ``permission``, either directly or via the groups they are in.

    :param user: The user to check permissions for
    :type user: :class:`~toja.models.user.User`
    :param permission: The permission to check for
    :type permission: ``str``
    """
    return permission in PERMISSIONS and user is not None and (permission in user.permissions or
                                                               (permission in PERMISSIONS_GROUPS and
                                                                PERMISSIONS_GROUPS[permission] in user.groups))


def permitted(request, permission):
    """Jinja2 filter that checks if the current user has a specific permission."""
    return has_permission(request.current_user, permission)


def require_permission(permissions):
    """Pyramid decorator to check permissions for a request."""
    def handler(f, *args, **kwargs):
        request = args[0]
        if has_permission(request.current_user, permissions):
            return f(*args, **kwargs)
        elif request.current_user:
            raise HTTPForbidden()
        else:
            raise HTTPFound(request.route_url('user.login', _query={'redirect': encode_route(request)}))
    return decorator(handler)


def includeme(config):
    """Inject the filters into the configuration."""
    config.get_jinja2_environment().filters['permitted'] = permitted
