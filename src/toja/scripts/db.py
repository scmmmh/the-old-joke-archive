import click
#import transaction

from pyramid.paster import (get_appsettings,setup_logging)

from ..models.meta import Base
from ..models import (get_engine, get_session_factory, get_tm_session)


@click.command()
@click.option('--drop-existing', is_flag=True, default=False, help='Drop the existing tables first')
@click.pass_context
def init_db(ctx, drop_existing):
    """Initialise the database structure"""
    config_uri = ctx.parent.params['config']
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    engine = get_engine(settings)
    if drop_existing:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    #session_factory = get_session_factory(engine)

    #with transaction.manager:
    #    dbsession = get_tm_session(session_factory, transaction.manager)

    #    model = MyModel(name='one', value=1)
    #    dbsession.add(model)
