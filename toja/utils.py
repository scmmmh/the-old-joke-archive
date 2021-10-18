"""Utility functions."""
import logging

from aiocouch import CouchDB
from email.message import EmailMessage
from email.utils import formatdate
from smtplib import SMTP
from tornado.web import HTTPError

logger = logging.getLogger(__name__)
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


def send_email(recipient: str, subject: str, body: str) -> None:
    """Send an email."""
    logger.debug('Sending e-mail')
    logger.debug(subject)
    logger.debug(body)
    if 'email' in config():
        with SMTP(config()['email']['server']) as smtp:
            if config()['email']['secure']:
                smtp.starttls()
            if 'auth' in config()['email']:
                smtp.login(config()['email']['auth']['user'], config()['email']['auth']['password'])
            email = EmailMessage()
            email.set_content(body)
            email['Subject'] = subject
            email['To'] = recipient
            email['From'] = config()['email']['sender']
            email['Date'] = formatdate()
            smtp.send_message(email)


class JSONAPIError(HTTPError):
    """Base class for JSONAPI errors."""

    def __init__(self: 'JSONAPIError', status_code: int, errors: list) -> 'JSONAPIError':
        """Construct a new JSONAPIError with the given ``errors``."""
        super().__init__(status_code)
        self.errors = errors

    def as_jsonapi(self: 'JSONAPIError') -> dict:
        """Format the errors as a JSONAPI error object."""
        return {'errors': self.errors}
