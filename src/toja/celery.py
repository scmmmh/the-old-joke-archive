from celery import Celery, bootsteps
from pyramid.paster import get_appsettings, setup_logging


app = Celery('toja', include=['toja.tasks'])


def includeme(config):
    """Handle the configuration from Pyramids"""
    settings = config.get_settings()
    app.conf.update(dict([(name[7:], value) for name, value in settings.items() if name.startswith('celery.')]))


# Code needed to set up loading configuration from the INI file instead of from celeryconfig.py
def add_worker_arguments(parser):
    """Adds the configuration parameter to the command-line."""
    parser.add_argument(
        '--configuration', default='development.ini',
        help='Path to the configuration INI.',
    )


app.user_options['worker'].add(add_worker_arguments)


class ConfigurationStep(bootsteps.Step):
    """Bootstep that configures the app from the commandline."""

    def __init__(self, worker, configuration=None, **options):
        if configuration:
            from .tasks.base import ConfiguredTask

            setup_logging(configuration)
            settings = get_appsettings(configuration)
            app.conf.update(dict([(name[7:], value) for name, value in settings.items() if name.startswith('celery.')]))

            ConfiguredTask._settings = settings


app.steps['worker'].add(ConfigurationStep)
