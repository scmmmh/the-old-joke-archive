"""TOJA command-line application."""
import click
import logging.config
import yaml
import os

from cerberus import Validator
from typing import Union

from ..server import run_application_server
from ..utils import set_config


CONFIG_SCHEMA = {
    'server': {
        'type': 'dict',
        'schema': {
            'host': {
                'type': 'string',
                'default': '127.0.0.1'
            },
            'port': {
                'type': 'integer',
                'default': 6543
            },
            'base': {
                'type': 'string',
                'default': 'http://127.0.0.1:6543'
            }
        },
        'default': {
            'host': '127.0.0.1',
            'port': 6543,
            'base': 'http://127.0.0.1:6543'
        }
    },
    'database': {
        'type': 'dict',
        'required': True,
        'schema': {
            'server': {
                'type': 'string',
                'default': 'http://localhost:5984'
            },
            'user': {
                'type': 'string'
            },
            'password': {
                'type': 'string'
            }
        }
    },
    'email': {
        'type': 'dict',
        'schema': {
            'server': {
                'type': 'string',
                'required': True,
                'empty': False,
            },
            'secure': {
                'type': 'boolean',
                'default': True,
            },
            'auth': {
                'type': 'dict',
                'schema': {
                    'user': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    },
                    'password': {
                        'type': 'string',
                        'required': True,
                        'empty': False,
                    }
                }
            },
            'sender': {
                'type': 'string',
                'default': 'automaton@oldjokearchive.com'
            }
        }
    },
    'debug': {
        'type': 'boolean',
        'default': False,
    },
    'logging': {
        'type': 'dict'
    }
}


def validate_config(config: dict) -> dict:
    """Validate the configuration.

    :param config: The configuration to validate
    :type config: dict
    :return: The validated and normalised configuration
    :rtype: dict
    """
    validator = Validator(CONFIG_SCHEMA)
    if validator.validate(config):
        return validator.normalized(config)
    else:
        error_list = []

        def walk_error_tree(err: Union[dict, list], path: str) -> None:
            if isinstance(err, dict):
                for key, value in err.items():
                    walk_error_tree(value, path + (str(key), ))
            elif isinstance(err, list):
                for sub_err in err:
                    walk_error_tree(sub_err, path)
            else:
                error_list.append(f'{".".join(path)}: {err}')

        walk_error_tree(validator.errors, ())
        error_str = '\n'.join(error_list)
        raise click.ClickException(f'Configuration errors:\n\n{error_str}')


@click.group()
def main() -> None:
    """Run the TOJA applications."""
    config = None
    if os.path.exists('config.yml'):
        with open('config.yml') as in_f:
            config = yaml.load(in_f, Loader=yaml.FullLoader)
    elif os.path.exists('/etc/toja/config.yml'):
        with open('/etc/toja/config.yml') as in_f:
            config = yaml.load(in_f, Loader=yaml.FullLoader)
    if not config:
        raise click.ClickException('No configuration found (./config.yml, /etc/toja/config.yml)')
    normalised = validate_config(config)
    set_config(normalised)
    if 'logging' in normalised:
        logging.config.dictConfig(normalised['logging'])


@click.command()
def server() -> None:
    """Run the TOJA server."""
    run_application_server()


main.add_command(server)


@click.command()
def background() -> None:
    """Run the TOJA background processing application."""
    pass


main.add_command(background)


@click.command()
def setup() -> None:
    """Set up the TOJA system."""
    pass


main.add_command(setup)
