from celery import Task

from ..models import get_engine, get_session_factory


class ConfiguredTask(Task):
    """Celery Task that provides access to a database session factory."""

    abstract = True

    _settings = None
    _dbsession = None

    @property
    def dbsession(self):
        """Return a new database session."""
        if self._dbsession is None and self._settings is not None:
            self._dbsession = get_session_factory(get_engine(self._settings))
        if self._dbsession:
            return self._dbsession()
        else:
            return None
