"""Classes for representing jokes."""
from .base import CouchDBBase


class Joke(CouchDBBase):
    """The database class for jokes."""

    name = 'jokes'
