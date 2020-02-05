import click


@click.command()
def cron():
    """Run regular maintenance tasks"""
    from ..tasks import clean_new_registrations

    clean_new_registrations.send()
