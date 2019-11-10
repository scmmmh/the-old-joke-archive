from collections import OrderedDict
from decorator import decorator
from functools import lru_cache
from pyramid.httpexceptions import HTTPForbidden, HTTPFound

from .models import User, Image
from .routes import encode_route


PERMISSIONS = OrderedDict((('admin.view', 'Access the Admin Interface'),
                           ('users.admin', 'Administer Users'),
                           ('sources.admin', 'Administer Sources'),
                           ('sources.new', 'Provide new Source Data')))
GROUPS = OrderedDict((('admin', ('admin.view', 'users.admin')),
                      ('data provider', ('sources.new', )),
                      ('data admin', ('admin.view', 'sources.admin'))))
PERMISSIONS_GROUPS = {}
for group, permissions in GROUPS.items():
    for permission in permissions:
        if permission in PERMISSIONS_GROUPS:
            PERMISSIONS_GROUPS[permission].add(group)
        else:
            PERMISSIONS_GROUPS[permission] = set([group])

OR = 1
AND = 2
STATIC = 3
DYNAMIC_ROUTE = 4
DYNAMIC_ID = 5


def class_lookup(class_name):
    if class_name == 'user':
        return User
    elif class_name == 'image':
        return Image
    raise Exception('Unknown class {0}'.format(class_name))


@lru_cache()
def compile_permission(permission):
    """Compile the permission string into a postfix notation. The permission string understands static permissions,
    which are provided as strings, dynamic permissions which are structured "@permission model_class matchdict_id",
    and the operators "and" and "or".

    :param permission: The permission string
    :type permission: ``str``
    :return: The permission as a
    """
    permission = permission.split()
    permission.reverse()
    tmp = []
    while permission:
        perm = permission.pop()
        if perm == 'or':
            tmp.append(OR)
        elif perm == 'and':
            tmp.append(AND)
        elif perm.startswith('@'):
            cls = class_lookup(permission.pop())
            oid = permission.pop()
            if oid.startswith(':'):
                tmp.append((DYNAMIC_ROUTE, perm[1:], cls, oid[1:]))
            else:
                tmp.append((DYNAMIC_ID, perm[1:], cls, oid))
        else:
            tmp.append((STATIC, perm))
    permission = []
    stack = []
    for perm in tmp:
        if isinstance(perm, tuple):
            permission.append(perm)
        else:
            if len(stack) == 0:
                stack.append(perm)
            else:
                permission.append(stack.pop())
                stack.append(perm)
    while stack:
        permission.append(stack.pop())
    return tuple(permission)


def check_permission(request, user, permission):
    """Checks whether the given ``user`` has the given ``permission``, either directly or via the groups they are in.

    :param request: The request to use for information about the current request
    :type request: :class:`pyramid.request.Request`
    :param user: The user to check permissions for
    :type user: :class:`~toja.models.user.User`
    :param permission: The permission to check for
    :type permission: ``str``
    """
    permission = compile_permission(permission)
    stack = []
    for perm in permission:
        if isinstance(perm, tuple):
            if perm[0] == STATIC:
                stack.append(user and perm[1] in PERMISSIONS and (perm[1] in user.permissions or
                                                                  (perm[1] in PERMISSIONS_GROUPS and
                                                                   len(PERMISSIONS_GROUPS[perm[1]].
                                                                       intersection(set(user.groups))) > 0)))
            elif perm[0] == DYNAMIC_ROUTE:
                obj = request.dbsession.query(perm[2]).filter(perm[2].id == request.matchdict[perm[3]]).first()
                if obj is not None:
                    stack.append(obj.allow(user, perm[1]))
                else:
                    stack.append(False)
            elif perm[0] == DYNAMIC_ID:
                obj = request.dbsession.query(perm[2]).filter(perm[2].id == perm[3]).first()
                if obj is not None:
                    stack.append(obj.allow(user, perm[1]))
                else:
                    stack.append(False)
            else:
                stack.append(False)
        elif perm == OR:
            stack.append(stack.pop() or stack.pop())
        elif perm == AND:
            stack.append(stack.pop() and stack.pop())
    if stack:
        return stack.pop()
    else:
        return False


def permitted(request, permission):
    """Jinja2 filter that checks if the current user has a specific permission."""
    return check_permission(request, request.current_user, permission)


def require_permission(permission):
    """Pyramid decorator to check permissions for a request."""
    def handler(f, *args, **kwargs):
        request = args[0]
        if check_permission(request, request.current_user, permission):
            return f(*args, **kwargs)
        elif request.current_user:
            raise HTTPForbidden()
        else:
            raise HTTPFound(request.route_url('user.login', _query={'redirect': encode_route(request)}))
    return decorator(handler)


def includeme(config):
    """Inject the filters into the configuration."""
    config.get_jinja2_environment().filters['permitted'] = permitted
