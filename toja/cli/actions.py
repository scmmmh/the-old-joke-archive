"""Single CLI action commands."""
import asyncio
import click

from ..actions import clean_old_user_tokens


@click.group()
def actions() -> None:
    """Run the TOJA background actions."""
    pass


@click.command()
def clean_user_tokens() -> None:
    """Clean old login tokens."""
    asyncio.run(clean_old_user_tokens())


actions.add_command(clean_user_tokens)
