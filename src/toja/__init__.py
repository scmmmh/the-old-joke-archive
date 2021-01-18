import os

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    os.environ['TOJA_WITHIN_WEBAPP'] = 'True'

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.commit()
    config.include('.tasks')
    config.include('.util')
    config.include('.config')
    config.include('.search')
    config.include('.models')
    config.include('.session')
    config.include('.permissions')
    config.include('.routes')
    config.include('.translation')
    config.include('.tests')
    config.scan()
    return config.make_wsgi_app()
