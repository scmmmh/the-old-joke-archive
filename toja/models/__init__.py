"""Database models."""
from aiocouch import CouchDB, exception


def connect_database(config: dict) -> CouchDB:
    """Connect to the database.

    :param config: The configuration to use for connecting
    :type config: dict
    :return: The CouchDB session
    :rtype: :class:`~aiocouch.CouchDB`
    """
    return CouchDB(server=config['database']['server'],
                   user=config['database']['user'],
                   password=config['database']['password'])


async def setup_database(config: dict) -> None:
    """Set up the database."""
    async with connect_database(config) as session:
        await session.check_credentials()
        try:
            await session['jokes']
        except exception.NotFoundError:
            await session.create('jokes')
        try:
            await session['users']
        except exception.NotFoundError:
            await session.create('users')
