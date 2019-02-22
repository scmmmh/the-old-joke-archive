import click


@click.command()
@click.option('-d', '--debug', is_flag=True, default=False)
@click.option('--sqlalchemy-url', default='')
def create_config():
    """Create a new configuration file."""
