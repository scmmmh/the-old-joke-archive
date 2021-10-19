"""The TOJA Server application."""
import logging

from tornado.web import Application, RedirectHandler
from tornado.ioloop import IOLoop

from .handlers import UserCollectionHandler, CollectionHandler, ItemHandler, LoginHandler, FrontendHandler
from ..models import Joke, User
from ..utils import config


logger = logging.getLogger(__name__)


def run_application_server() -> None:
    """Run the TOJA server.

    :param config: The configuration to use
    :type config: dict
    """
    logger.debug('Application server starting up...')
    app = Application(
        [
            ('/', RedirectHandler, {'permanent': False, 'url': '/app'}),
            ('/app(.*)', FrontendHandler),
            ('/api/users', UserCollectionHandler),
            ('/api/users/_login', LoginHandler),
            (r'/api/users/([a-z0-9\-]+)', ItemHandler, {'type': User}),
            ('/api/jokes', CollectionHandler, {'type': Joke}),
            (r'/api/jokes/([a-z0-9\-]+)', ItemHandler, {'type': Joke})
        ],
        debug=config()['debug'],
        xsrf_cookies=True,
        cookie_secret='ohqu6aegezie9uuChiaf9shuisahsiegiej4Quo9aiK3Ohhe8eisoimig4Bee9Eb')
    logger.debug(f'Application listening on {config()["server"]["host"]} port {config()["server"]["port"]}')
    app.listen(config()['server']['port'], config()['server']['host'])
    IOLoop.current().start()
