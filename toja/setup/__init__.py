"""Set up the TOJA storage backends."""
import logging
import logging.config

from aiocouch import exception

from ..utils import couchdb


logger = logging.getLogger(__name__)

DATABASES = [
    '_users',
    '_replicator',
    {
        'name': 'users',
        'indices': {
            'email': [
                {'email': 'asc'},
                {'name': 'asc'},
            ]
        }
    }
]


async def async_setup() -> None:
    """Run an asynchronous setup process."""
    async with couchdb() as session:
        for db_config in DATABASES:
            if isinstance(db_config, str):
                try:
                    logger.debug(f'Creating database {db_config}')
                    await session.create(db_config)
                except exception.PreconditionFailedError:
                    pass
            elif isinstance(db_config, dict):
                try:
                    logger.debug(f'Creating database {db_config["name"]}')
                    await session.create(db_config['name'])
                except exception.PreconditionFailedError:
                    pass
                db = await session[db_config['name']]
                if 'indices' in db_config:
                    for idx_name, idx_config in db_config['indices'].items():
                        await db._remote._post(f'/{db_config["name"]}/_index', {
                            'index': {
                                'fields': idx_config,
                            },
                            'name': f'{db_config["name"]}-{idx_name}-idx',
                            'type': 'json'
                        })
