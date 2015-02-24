import numpy
import matplotlib.pyplot as plt
import mpld3
import os
import logging
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config
from waitress import serve
import psycopg2
from contextlib import closing
from pyramid.events import NewRequest, subscriber
import datetime as dt
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound, HTTPInternalServerError
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import remember, forget
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from zope.sqlalchemy import ZopeTransactionExtension
import pprint

USER = 'chatzis'
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'incidents'
    gid = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    units = sa.Column(sa.UnicodeText, nullable=False)
    date_time = sa.Column(sa.UnicodeText, nullable=False)
    incident_type = sa.Column(sa.UnicodeText, nullable=False)

    def __repr__(self):
        return u"{}: {}".format(self.__class__.__name__, self.title)

    @classmethod
    def all_incident(cls, incident):
        return DBSession.query(cls).order_by(cls.created.desc()).all()

    @classmethod
    def newest_entry(cls):
        return DBSession.query(cls).order_by(cls.created.desc()).first()

    @classmethod
    def all_type(cls, itype):
        return DBSession.query(cls).filter(cls.type == itype).all()

    def update_from_request(self, request):
        self.title = request.params.get('title', None)
        self.text = request.params.get('text', None)

    def render_markdown(self):
        return markdown.markdown(
            self.text, extensions=['codehilite', 'fenced_code'])

    def convert_strftime(self):
        return self.created.strftime('%b %d, %Y')

    def json(self):
        return {'title': self.title,
                'text': self.render_markdown(),
                'created': self.created.strftime('%b %d, %Y'),
                'id': self.id}

    def json_edit_get(self):
        return {'title': self.title,
                'text': self.text,
                'created': self.created.strftime('%b %d, %Y'),
                'id': self.id}


def main():
    """Create a configured wsgi app"""
    settings = {}
    settings['reload_all'] = os.environ.get('DEBUG', True)
    settings['debug_all'] = os.environ.get('DEBUG', True)
    settings['sqlalchemy.url'] = os.environ.get(
        'DATABASE_URL',
        'postgresql://{}:@localhost:5432/seattle'.format(USER)
    )
    engine = sa.engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    settings['auth.username'] = os.environ.get('AUTH_USERNAME', 'admin')
    # secret value for session signing:
    secret = os.environ.get('JOURNAL_SESSION_SECRET', 'itsaseekrit')
    session_factory = SignedCookieSessionFactory(secret)
    # add a secret value for auth tkt signing
    auth_secret = os.environ.get('JOURNAL_AUTH_SECRET', 'anotherseekrit')
    # configuration setup
    config = Configurator(
        settings=settings,
        session_factory=session_factory,
        authentication_policy=AuthTktAuthenticationPolicy(
            secret=auth_secret,
            hashalg='sha512'
        ),
        authorization_policy=ACLAuthorizationPolicy(),
    )
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')
    config.scan()
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    main()
    entry = Entry.all_type('Aid Response')
    pprint.pprint(entry)
    plt.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
    mpld3.show()
