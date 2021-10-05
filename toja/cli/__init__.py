"""TOJA command-line application."""
import click


@click.group()
def main() -> None:
    """Run the TOJA applications."""
    pass


@click.command()
def server() -> None:
    """Run the TOJA server."""
    pass


main.add_command(server)


@click.command()
def background() -> None:
    """Run the TOJA background processing application."""
    pass


main.add_command(background)
