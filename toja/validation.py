"""Validation functionality."""
import logging

from cerberus import Validator
from cerberus.errors import ValidationError
from email_validator import validate_email, EmailNotValidError
from typing import Union, List

from .utils import JSONAPIError


logger = logging.getLogger(__name__)


class ValidationError(JSONAPIError):
    """Validation error that provides JSONAPI compatible error messages."""

    def __init__(self: 'ValidationError', errors: List[ValidationError]) -> 'ValidationError':
        """Create a new ValidationError.

        This will automatically convert the Cerberus errors into the JSONAPI error structure.
        """
        flat_errors = []

        def flatten(key: str, value: Union[dict, list, str], path: str = '') -> None:
            if isinstance(value, list):
                for part in value:
                    flatten(key, part, path=path)
            elif isinstance(value, dict):
                for part_key, part_value in value.items():
                    flatten(part_key, part_value, path=f'{path}.{key}')
            else:
                path = f'{path}.{key}'.strip('.')
                flat_errors.append({
                    'title': value[0].capitalize() + value[1:],
                    'source': {
                        'pointer': path
                    }
                })

        for key, value in errors.items():
            flatten(key, value)

        super().__init__(400, flat_errors)


class TojaValidator(Validator):
    """Extended cerberus Validator."""

    def _check_with_validate_email(self: 'TojaValidator', field: str, value: str) -> None:
        """Validate an e-mail address."""
        try:
            validate_email(value)
        except EmailNotValidError as enve:
            self._error(field, str(enve))

    def _normalize_coerce_email(self: 'TojaValidator', value: 'str') -> str:
        """Normalise an e-mail address."""
        try:
            valid = validate_email(value)
            return valid.email.lower()
        except EmailNotValidError:
            return value


def validate(schema: dict, data: dict, purge_unknown: bool = False) -> dict:
    """Validate the given ``data`` using the ``schema``."""
    validator = TojaValidator(schema, purge_unknown=purge_unknown)
    if not validator.validate(data):
        logger.debug(validator.errors)
        raise ValidationError(validator.errors)
    return validator.document


def object_schema(type_name: str, id_value: Union[str, None] = None,
                  attributes: Union[dict, None] = None, relationships: Union[dict, None] = None) -> dict:
    """Create a full object schema."""
    obj = {
        'type': type_schema(type_name),
        'id': id_schema(id_value),
    }
    if attributes is not None:
        obj['attributes'] = {
            'type': 'dict',
            'required': True,
            'schema': attributes,
        }
    if relationships is not None:
        obj['relationships'] = {
            'type': 'dict',
            'required': True,
            'schema': relationships,
        }
    return obj


def type_schema(type_name: str) -> dict:
    """Return a cerberus schema for JSONAPI type entries."""
    return {
        'type': 'string',
        'required': True,
        'empty': False,
        'allowed': [type_name],
    }


def id_schema(value: Union[str, None] = None) -> dict:
    """Return a cerberus schema for JSONAPI id entries."""
    if value:
        return {
            'type': 'string',
            'required': True,
            'empty': False,
            'allowed': [value]
        }
    else:
        return {
            'type': 'string',
            'required': True,
            'empty': False,
        }


def one_to_one_relationship_schema(type_name: str, value: Union[str, None] = None) -> dict:
    """Return a cerberus schema for a one-to-one JSONAPI relationship."""
    return {
        'type': 'dict',
        'required': True,
        'empty': False,
        'schema': {
            'data': {
                'type': 'dict',
                'required': True,
                'empty': False,
                'schema': {
                    'type': type_schema(type_name),
                    'id': id_schema(value),
                }
            }
        }
    }
