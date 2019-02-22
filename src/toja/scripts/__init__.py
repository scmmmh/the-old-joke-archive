import click

from .config import create_config
from .db import init_db


@click.group()
@click.option('-c', '--config', default='production.ini')
def main(config):
    """Administration Utility for TOJA"""

main.add_command(create_config)
main.add_command(init_db)
