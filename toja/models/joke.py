"""Classes for representing jokes."""
from .base import Base


class Joke(Base):
    """The database class for jokes."""

    name = 'jokes'
