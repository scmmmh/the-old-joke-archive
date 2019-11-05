import dramatiq

from .middleware import ConfigMiddleware, DBSessionMiddleware
from .ocr import run_ocr  # noqa


dramatiq.get_broker().add_middleware(ConfigMiddleware())
dramatiq.get_broker().add_middleware(DBSessionMiddleware())
