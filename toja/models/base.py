"""Base database access methods."""
import json

from aiohttp import ClientSession, BasicAuth
from copy import deepcopy
from typing import Union


class CouchDBBase():
    """Base class for all CouchDB types."""

    def __init__(self: 'CouchDBBase', id_: Union[str, None] = None,
                 attributes: Union[dict, None] = None) -> 'CouchDBBase':
        """Create a new object instance."""
        self._id = id_
        self._attributes = deepcopy(attributes) if attributes is not None else {}

    @classmethod
    def from_jsonapi(cls: 'CouchDBBase', obj: dict) -> 'CouchDBBase':
        """Load the object from a JSONAPI representation."""
        id_ = None
        if '_id' in obj:
            id_ = obj['_id']
        attributes = None
        if 'attributes' in obj:
            attributes = deepcopy(obj['attributes'])
        return cls(id_=id_, attributes=attributes)

    def as_jsonapi(self: 'CouchDBBase') -> dict:
        """Return the object in JSONAPI representation."""
        obj = {
            'type': self.name,
            'attributes': self._attributes
        }
        if self._id:
            obj['id'] = self._id
        return obj

    @classmethod
    def from_couchdb(cls: 'CouchDBBase', obj: dict) -> 'CouchDBBase':
        """Load the object from the CouchDB representation."""
        obj = deepcopy(obj)
        id_ = obj['_id']
        for key in list(obj.keys()):
            if key.startswith('_'):
                del obj[key]
        return cls(id_=id_, attributes=obj)

    def as_couchdb(self: 'CouchDBBase') -> dict:
        """Return the object in CouchDB representation."""
        obj = deepcopy(self._attributes)
        if self._id:
            obj['_id'] = self._id
        return obj


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

    async def execute(self, method: str, path: str, body: Union[str, None] = None) -> dict:  # noqa: ANN101
        """Execute the given query.

        :param method: The request method
        :type method: str
        :param path: The request path
        :type path: str
        """
        result = await self._client_session.request(method=method,
                                                    url=f'{self._config["database"]["server"]}{path}',
                                                    auth=self._auth,
                                                    data=body,
                                                    headers={'Content-Type': 'application/json'})
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
        return self._type.from_couchdb(await self._session.execute('GET', f'/{self._type.name}/{id_}'))

    async def create(self: 'Query', obj: CouchDBBase) -> CouchDBBase:
        """Create a single instance."""
        result = await self._session.execute('POST', f'/{self._type.name}', body=json.dumps(obj.as_couchdb()))
        return await self.single(result['id'])


class NotFoundError(Exception):
    """Error message to indicate that the requested resource is not found in the database."""

    def __init__(self, message: str):  # noqa: ANN101, ANN204
        """Initialise the error message."""
        self._message = message

    def __str__(self) -> str:  # noqa: ANN101
        """Return a human-readable error message."""
        return self._message
