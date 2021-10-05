"""Base database access methods."""
from aiohttp import ClientSession, BasicAuth


class CouchDBBase():
    """Base class for all CouchDB types."""

    pass


class Session():
    """Database session for performing queries."""

    def __init__(self, config: dict):  # noqa: ANN101, ANN204
        """Initialise the database session."""
        self._config = config
        self._client_session = ClientSession()
        self._auth = BasicAuth(self._config['database']['user'], self._config['database']['password'])

    def query(self, type_: CouchDBBase) -> 'Query':  # noqa: ANN101
        """Query for the specifiy ``type_``."""
        return Query(self, type_)

    async def execute(self, method: str, path: str) -> CouchDBBase:  # noqa: ANN101
        """Execute the given query.

        :param method: The request method
        :type method: str
        :param path: The request path
        :type path: str
        """
        result = await self._client_session.request(method=method,
                                                    url=f'{self._config["database"]["server"]}{path}',
                                                    auth=self._auth)
        if result.status == 404:
            raise NotFoundError(f'{path}')
        return await result.json()


class Query():
    """Query builder object."""

    def __init__(self, session: Session, type_: CouchDBBase):  # noqa: ANN101, ANN204
        """Initialise the query builder."""
        self._session = session
        self._type = type_

    async def single(self, id_: str) -> CouchDBBase:  # noqa: ANN101
        """Query for a single instance by ``id_``."""
        await self._session.execute('GET', f'/{self._type.name}/{id_}')


class NotFoundError(Exception):
    """Error message to indicate that the requested resource is not found in the database."""

    def __init__(self, message: str):  # noqa: ANN101, ANN204
        """Initialise the error message."""
        self._message = message

    def __str__(self) -> str:  # noqa: ANN101
        """Return a human-readable error message."""
        return self._message
