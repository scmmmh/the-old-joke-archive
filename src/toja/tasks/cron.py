import dramatiq

from datetime import datetime, timedelta
from sqlalchemy import and_

from .middleware import DBSessionMiddleware
from ..models import User


@dramatiq.actor()
def clean_new_registrations():
    """Clean all new :class:`~toja.models.user.User` registrations that are older than 48 hours.

    This is a dramatiq Actor, so can be run in the background.
    """
    cutoff = datetime.utcnow() - timedelta(days=2)
    dbsession = DBSessionMiddleware.dbsession()
    dbsession.query(User).filter(and_(User.status == 'new', User.created < cutoff)).delete()
