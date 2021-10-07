"""Validation functionality."""
from cerberus import Validator
from cerberus.errors import ValidationError
from email_validator import validate_email, EmailNotValidError
from typing import Union, List


class ValidationError(Exception):
    """Validation error that provides JSONAPI compatible error messages."""

    def __init__(self: 'ValidationError', errors: List[ValidationError]) -> 'ValidationError':
        """Create a new ValidationError.

        This will automatically convert the Cerberus errors into the JSONAPI error structure.
        """
        super().__init__(self, 'Validation error')
        self.errors = []

        def flatten(key: str, value: Union[dict, list, str], path: str = '') -> None:
            if isinstance(value, list):
                for part in value:
                    flatten(key, part, path=path)
            elif isinstance(value, dict):
                for part_key, part_value in value.items():
                    flatten(part_key, part_value, path=f'{path}.{key}')
            else:
                path = f'{path}.{key}'.strip('.')
                self.errors.append({
                    'title': value[0].capitalize() + value[1:],
                    'source': {
                        'pointer': path
                    }
                })

        for key, value in errors.items():
            flatten(key, value)


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
