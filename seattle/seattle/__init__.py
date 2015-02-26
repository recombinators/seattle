from pyramid.config import Configurator
from sqlalchemy import engine_from_config
# import os

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('index', '/')
    config.add_route('index_lat_long', '{lat}/{lon}')
    config.add_route('ajax', 'ajax/{lat}/{lon}')
    # config.add_route('histo', '/histo')
    # config.add_route('line', 'line')
    config.scan()
    return config.make_wsgi_app()
