"""Test utility functions."""
from aiocouch import Document
from typing import AsyncGenerator


def auth_token(user: Document) -> str:
    """Return the authentication token for the given user."""
    return f'{user["_id"]}$${user["tokens"][0]["token"]}'


async def async_gen_to_list(generator: AsyncGenerator) -> list:
    """Transform the values of an async generator into a list."""
    items = []
    async for item in generator:
        items.append(item)
    return items
