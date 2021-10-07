"""Utility functions."""
from aiocouch import CouchDB


_config = {}


def set_config(config: dict) -> None:
    """Set the global configuration."""
    global _config
    _config = config


def config() -> dict:
    """Get the global configuration."""
    return _config


def couchdb() -> CouchDB:
    """Get a CouchDB instance."""
    return CouchDB(config()['database']['server'],
                   config()['database']['user'],
                   config()['database']['password'])
