"""The TOJA Server application."""
import logging

from tornado.web import Application
from tornado.ioloop import IOLoop

from .api import CollectionHandler, ItemHandler
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
            ('/api/users', CollectionHandler, {'config': config, 'type': Joke}),
            ('/api/users/([0-9]+)', ItemHandler, {'config': config, 'type': Joke}),
            ('/api/jokes', CollectionHandler, {'config': config, 'type': Joke}),
            ('/api/jokes/([0-9]+)', ItemHandler, {'config': config, 'type': Joke})
        ],
        debug=config['debug'])
    logger.debug(f'Application listening on {config["server"]["host"]} port {config["server"]["port"]}')
    app.listen(config['server']['port'], config['server']['host'])
    IOLoop.current().start()
