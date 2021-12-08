"""Test utility functions."""
from aiocouch import Document


def auth_token(user: Document) -> str:
    """Return the authentication token for the given user."""
    return f'{user["_id"]}$${user["tokens"][0]["token"]}'
