import dramatiq

from .middleware import ConfigMiddleware, DBSessionMiddleware, ElasticsearchMiddleware
from .cron import clean_new_registrations  # noqa
from .ocr import run_ocr  # noqa
from .search import index_all  # noqa


dramatiq.get_broker().add_middleware(ConfigMiddleware())
dramatiq.get_broker().add_middleware(DBSessionMiddleware())
dramatiq.get_broker().add_middleware(ElasticsearchMiddleware())
