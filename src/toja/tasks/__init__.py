import os
import dramatiq

from pyramid.paster import get_appsettings

from .middleware import ConfigMiddleware, DBSessionMiddleware, ElasticsearchMiddleware


def setup_broker(settings):
    """Setup all brokers."""
    from dramatiq.brokers.redis import RedisBroker

    dramatiq.set_broker(RedisBroker(url=settings['app.broker.url']))
    dramatiq.get_broker().add_middleware(ConfigMiddleware())
    dramatiq.get_broker().add_middleware(DBSessionMiddleware())
    dramatiq.get_broker().add_middleware(ElasticsearchMiddleware())


def includeme(config):
    setup_broker(config.get_settings())


if 'TOJA_WITHIN_WEBAPP' not in os.environ:
    config_uri = os.environ['TOJA_CONFIGURATION_URI'] if 'TOJA_CONFIGURATION_URI' in os.environ \
        else 'production.ini'

    setup_broker(get_appsettings(config_uri))

    from .cron import *  # noqa
    from .joke import *  # noqa
    from .ocr import *  # noqa
    from .search import *  # noqa
