import os
import dramatiq

if 'TOJA_WITHIN_WEBAPP' not in os.environ:
    from dramatiq.brokers.redis import RedisBroker
    from pyramid.paster import get_appsettings, setup_logging

    config_uri = os.environ['TOJA_CONFIGURATION_URI'] if 'TOJA_CONFIGURATION_URI' in os.environ \
        else 'production.ini'
    setup_logging(config_uri)
    dramatiq.set_broker(RedisBroker(url=get_appsettings(config_uri)['app.broker.url']))

from .middleware import ConfigMiddleware, DBSessionMiddleware, ElasticsearchMiddleware  # noqa
from .cron import clean_new_registrations  # noqa
from .joke import process_all_jokes, process_joke  # noqa
from .ocr import run_ocr  # noqa
from .search import index_all, index_joke  # noqa

dramatiq.get_broker().add_middleware(ConfigMiddleware())
dramatiq.get_broker().add_middleware(DBSessionMiddleware())
dramatiq.get_broker().add_middleware(ElasticsearchMiddleware())
