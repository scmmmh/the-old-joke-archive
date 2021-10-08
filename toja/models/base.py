"""Base database access methods."""
from aiocouch import CouchDB
from copy import deepcopy
from typing import Union, List

from ..validation import TojaValidator, ValidationError


class Base():
    """Base class for all database models."""

    def __init__(self: 'Base', id_: Union[str, None] = None,
                 attributes: Union[dict, None] = None) -> 'Base':
        """Create a new object instance."""
        self._id = id_
        self._attributes = deepcopy(attributes) if attributes is not None else {}

    @classmethod
    def validate_create(cls: 'Base', obj: dict) -> dict:
        """Validate the ``obj`` as input for creating a new instance."""
        validator = TojaValidator(cls.create_schema)
        if not validator.validate(obj):
            raise ValidationError(validator.errors)
        return validator.document

    @classmethod
    def from_jsonapi(cls: 'Base', obj: dict) -> 'Base':
        """Load the object from a JSONAPI representation."""
        id_ = None
        if 'id' in obj:
            id_ = obj['id']
        attributes = {}
        if 'attributes' in obj:
            attributes = obj['attributes']
        return cls(id_=id_, attributes=attributes)

    def as_jsonapi(self: 'Base') -> dict:
        """Return the object in JSONAPI representation."""
        obj = {
            'type': self.name,
            'attributes': self._attributes
        }
        if self._id:
            obj['id'] = self._id
        return obj

    @classmethod
    def from_couchdb(cls: 'Base', obj: dict) -> 'Base':
        """Load the object from the CouchDB representation."""
        id_ = obj['_id']
        for key in list(obj.keys()):
            if key.startswith('_'):
                del obj[key]
        return cls(id_=id_, attributes=dict(obj))

    def as_couchdb(self: 'Base') -> dict:
        """Return the object in CouchDB representation."""
        obj = deepcopy(self._attributes)
        if self._id:
            obj['_id'] = self._id
        return obj

    async def check_unique(self: 'Base', db: CouchDB) -> None:
        """Check any unique constraints."""
        pass

    async def pre_create(self: 'Base', db: CouchDB) -> None:
        """Run any pre-creation steps."""
        pass

    async def post_create(self: 'Base', db: CouchDB) -> None:
        """Run any post-creation steps."""
        pass

    def allow_access(self: 'Base', action: str, user_id: str, groups: List[str]) -> bool:
        """Check that access is allowed for the action, user_id, and groups."""
        return True
