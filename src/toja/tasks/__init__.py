import dramatiq

from .middleware import ConfigMiddleware, DBSessionMiddleware, ElasticsearchMiddleware
from .cron import clean_new_registrations  # noqa
from .joke import process_joke  # noqa
from .ocr import run_ocr  # noqa
from .search import index_all, index_joke  # noqa


dramatiq.get_broker().add_middleware(ConfigMiddleware())
dramatiq.get_broker().add_middleware(DBSessionMiddleware())
dramatiq.get_broker().add_middleware(ElasticsearchMiddleware())
