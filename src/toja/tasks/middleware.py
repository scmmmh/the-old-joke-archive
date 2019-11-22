import dramatiq
import os
import transaction

from elasticsearch_dsl import connections
from pyramid.paster import get_appsettings, setup_logging
from threading import local

from toja.models import get_engine, get_tm_session, get_session_factory
from toja.util import convert_type


CACHED_SETTINGS = {}


class ConfigMiddleware(dramatiq.Middleware):
    """The :class:`~toja.tasks.ConfigMiddleware` is a dramatiq :class:`~dramatiq.middleware.Middleware` that provides
    access to the application configuration. Requires that the ``TOJA_CONFIGURATION_URI`` environment variable
    contains the path to the configuration file.
    """

    state = local()
    _settings = None

    @classmethod
    def settings(cls):
        """Class method to access the settings object."""
        return getattr(cls.state, 'settings', {})

    @classmethod
    def config_setting(cls, key, target_type=None, default=None):
        """Class method to access a specific config setting key.

        :param request: The request used to access the configuration settings
        :type request: :class:`~pyramid.request.Request`
        :param key: The configuration key
        :type key: `unicode`
        :param target_type: If specified, will convert the configuration setting
                            to the given type using :func:`~toja.util.convert_type`
        :type default: The default value to return if there is no setting with the
                       given key
        :return: The configuration setting value or ``default``
        """
        global CACHED_SETTINGS
        if key in CACHED_SETTINGS:
            return CACHED_SETTINGS[key]
        else:
            if key in cls.settings():
                if target_type:
                    CACHED_SETTINGS[key] = convert_type(cls.settings()[key], target_type, default=default)
                else:
                    CACHED_SETTINGS[key] = cls.settings()[key]
            else:
                CACHED_SETTINGS[key] = default
        return cls.config_setting(key, target_type=target_type, default=default)

    def before_worker_boot(self, broker, worker):
        """Before the worker boots, load the configuration settings."""
        config_uri = os.environ['TOJA_CONFIGURATION_URI'] if 'TOJA_CONFIGURATION_URI' in os.environ \
            else 'production.ini'
        setup_logging(config_uri)
        setattr(self.state, 'settings', get_appsettings(config_uri))
        self._settings = get_appsettings(config_uri)

    def before_process_message(self, broker, message):
        """Before the message is processed, load the configuration settings for the thread. Re-uses the settings
        loaded in :func:`~toja.tasks.middleware.ConfigMiddleware.before_worker_boot`."""
        if self._settings:
            setattr(self.state, 'settings', self._settings)
        else:
            config_uri = os.environ['TOJA_CONFIGURATION_URI'] if 'TOJA_CONFIGURATION_URI' in os.environ \
                else 'production.ini'
            setup_logging(config_uri)
            setattr(self.state, 'settings', get_appsettings(config_uri))

    def after_process_message(self, broker, message, *, result=None, exception=None):
        delattr(self.state, 'settings')

    after_skip_message = after_process_message


class DBSessionMiddleware(dramatiq.Middleware):
    """The :class:`~toja.tasks.middleware.DBSessionMiddleware` is a dramatiq :class:`~dramatiq.middleware.Middleware`
    that wraps the actor with a transaction, which is automatically commited, if the actor is successful, or performs
    an abort, if the actor throws an exception.
    """

    state = local()

    @classmethod
    def dbsession(cls):
        """Class method to fetch the database session."""
        return getattr(cls.state, 'dbsession', None)

    def before_worker_boot(self, broker, worker):
        """Initialise the session factory before whe worker boots."""
        self.__session_factory = get_session_factory(get_engine(ConfigMiddleware.settings()))

    def before_process_message(self, broker, message):
        """Before beginning to process a message, start the session and add it to the thread local state."""
        transaction.manager.begin()
        setattr(self.state, 'dbsession', get_tm_session(self.__session_factory, transaction.manager))

    def after_process_message(self, broker, message, *, result=None, exception=None):
        """After the process completes, if no exception is thrown, commit the transaction, else abort."""
        if exception is None:
            transaction.manager.commit()
        else:
            transaction.manager.abort()
        delattr(self.state, 'dbsession')

    after_skip_message = after_process_message


class ElasticsearchMiddleware(dramatiq.Middleware):
    """The :class:`~toja.tasks.middleware.ElasticsearchMiddleware` is a dramatiq
    :class:`~dramatiq.middleware.Middleware` that sets up the Elasticsearch connection for the worker.
    """

    def before_worker_boot(self, broker, worker):
        connections.create_connection(hosts=convert_type(ConfigMiddleware.settings()['app.elasticsearch.hosts'], 'list'))
