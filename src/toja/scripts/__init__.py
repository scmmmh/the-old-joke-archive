import click
import os

from pyramid.paster import get_appsettings, setup_logging

from .config import create_config
from .db import init_db
from .cron import cron


@click.group()
@click.option('-c', '--config', default='production.ini')
@click.pass_context
def main(ctx, config):
    """Administration Utility for TOJA"""
    os.environ['TOJA_WITHIN_WEBAPP'] = 'True'
    from ..tasks import setup_broker  # noqa
    try:
        setup_logging(config)
        settings = get_appsettings(config)
        ctx.obj = {'settings': settings}
        setup_broker(settings)
    except FileNotFoundError:
        pass


main.add_command(create_config)
main.add_command(init_db)
main.add_command(cron)
