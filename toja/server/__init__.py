"""The TOJA Server application."""
import logging

from tornado.web import Application, RedirectHandler
from tornado.ioloop import IOLoop

from .handlers import CollectionHandler, ItemHandler, FrontendHandler
from ..models import Joke


logger = logging.getLogger(__name__)


def run_application_server(config: dict) -> None:
    """Run the TOJA server.

    :param config: The configuration to use
    :type config: dict
    """
    logger.debug('Application server starting up...')
    app = Application(
        [
            ('/', RedirectHandler, {'permanent': False, 'url': '/app'}),
            ('/app(.*)', FrontendHandler),
            ('/api/users', CollectionHandler, {'config': config, 'type': Joke}),
            ('/api/users/([a-z0-9]+)', ItemHandler, {'config': config, 'type': Joke}),
            ('/api/jokes', CollectionHandler, {'config': config, 'type': Joke}),
            ('/api/jokes/([a-z0-9]+)', ItemHandler, {'config': config, 'type': Joke})
        ],
        debug=config['debug'])
    logger.debug(f'Application listening on {config["server"]["host"]} port {config["server"]["port"]}')
    app.listen(config['server']['port'], config['server']['host'])
    IOLoop.current().start()
