PERMISSIONS = ['sources.upload']
GROUPS = {'admin': ['sources.upload']}
PERMISSIONS_GROUPS = dict([permission, group] for group, permissions in GROUPS.items() for permission in permissions)


def has_permission(user, permission):
    """Checks whether the given ``user`` has the given ``permission``, either directly or via the groups they are in.

    :param user: The user to check permissions for
    :type user: :class:`~toja.models.user.User`
    :param permission: The permission to check for
    :type permission: ``str``
    """
    return permission in PERMISSIONS and user is not None and (permission in user.permissions or
        (permission in PERMISSIONS_GROUPS and PERMISSIONS_GROUPS[permission] in user.groups))


def permitted(request, permission):
    """Jinja2 filter that checks if the current user has a specific permission."""
    return has_permission(request.current_user, permission)


def logged_in(request):
    """Jinja2 filter that checks if the current user is logged in."""
    return request.current_user is not None


def includeme(config):
    """Inject the filters into the configuration."""
    config.get_jinja2_environment().filters['permitted'] = permitted
    config.get_jinja2_environment().filters['logged_in'] = logged_in
