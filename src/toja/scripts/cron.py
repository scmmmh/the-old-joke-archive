import click

from ..tasks import clean_new_registrations


@click.command()
def cron():
    """Run regular maintenance tasks"""
    clean_new_registrations.send()
