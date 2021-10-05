"""Database models."""
from .base import Session, NotFoundError  # noqa
from .joke import Joke  # noqa


session_singleton = None


def get_session(config: dict) -> Session:
    """Get the database session.

    A singleton database session is provided.
    """
    global session_singleton

    if session_singleton is None:
        session_singleton = Session(config)
    return session_singleton


async def setup_database(config: dict) -> None:
    """Set up the database."""
