"""The TOJA Server application."""
import logging

from tornado.web import Application, RedirectHandler
from tornado.ioloop import IOLoop

from .handlers import (UserCollectionHandler, UserItemHandler, LoginHandler, ResetPasswordHandler, FrontendHandler,
                       SourceCollectionHandler, SourceItemHandler, JokeCollectionHandler, JokeItemHandler,
                       JokeDataHandler, joke_html_injector, SearchHandler, SearchExactCountsHandler, SuggestionHandler,
                       AdminSearchHandler)
from ..utils import config


logger = logging.getLogger(__name__)


def run_application_server() -> None:
    """Run the TOJA server.

    :param config: The configuration to use
    :type config: dict
    """
    logger.debug('Application server starting up...')
    routes = [
        ('/', RedirectHandler, {'permanent': False, 'url': '/app'}),
        ('/app(.*)', FrontendHandler, {'html_injectors': {r'/jokes/([a-z0-9\-]+)': joke_html_injector}}),
        ('/api/users', UserCollectionHandler),
        ('/api/users/_login', LoginHandler),
        ('/api/users/_reset-password', ResetPasswordHandler),
        (r'/api/users/([a-z0-9\-]+)', UserItemHandler),
        ('/api/sources', SourceCollectionHandler),
        (r'/api/sources/([a-z0-9\-]+)', SourceItemHandler),
        ('/api/jokes', JokeCollectionHandler),
        (r'/api/jokes/([a-z0-9\-]+)', JokeItemHandler),
        (r'/api/jokes/([a-z0-9\-]+)/image', JokeDataHandler),
        ('/api/search', SearchHandler),
        ('/api/search/exhaustive-counts', SearchExactCountsHandler),
        ('/api/suggest/([a-z_]+)', SuggestionHandler),
        ('/api/admin/search', AdminSearchHandler),
    ]
    if config()['test']:
        from .handlers.test import TestHandler
        routes.append(('/test', TestHandler))
    app = Application(
        routes,
        debug=config()['debug'],
        xsrf_cookies=True,
        xsrf_cookie_kwargs={'secure': False if config()['debug'] else True, 'samesite': 'strict'},
        cookie_secret='ohqu6aegezie9uuChiaf9shuisahsiegiej4Quo9aiK3Ohhe8eisoimig4Bee9Eb')
    logger.debug(f'Application listening on {config()["server"]["host"]} port {config()["server"]["port"]}')
    app.listen(config()['server']['port'], config()['server']['host'])
    IOLoop.current().start()
