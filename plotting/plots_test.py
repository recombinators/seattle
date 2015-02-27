import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
import os
import math
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
import time
import pytz
utc = pytz.timezone('UTC')


USER = 'chatzis'
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class PST(dt.tzinfo):

    def utcoffset(self, dat):
        return dt.timedelta(hours=-8)

    def dst(self, dat):
        return dt.timedelta(0)


class Entry(Base):
    __tablename__ = 'incidents'
    gid = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    units = sa.Column(sa.UnicodeText, nullable=False)
    date_time = sa.Column(sa.DateTime, nullable=False)
    incident_type = sa.Column(sa.UnicodeText, nullable=False)
    address = sa.Column(sa.UnicodeText, nullable=False)
    incident_number = sa.Column(sa.UnicodeText, nullable=False)
    latitude = sa.Column(sa.UnicodeText, nullable=False)
    longitude = sa.Column(sa.UnicodeText, nullable=False)
    the_geom = sa.Column(sa.UnicodeText, nullable=False)

    def __repr__(self):
        return u"{}: {}".format(self.__class__.__name__, self.incident_type)

    @classmethod
    def all_type(cls, itype):
        return DBSession.query(cls).filter(cls.incident_type == itype).limit(1000)

    def json(self):
        utc_dt = utc.normalize(self.date_time.astimezone(utc))
        return {'incident_type': self.incident_type,
                'date_time': time.mktime(utc_dt.timetuple()),
                }

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
    dates = []
    for i in entry:
        dates.append(i.json()['date_time'])
        pprint.pprint(i.json()['date_time'])

    pprint.pprint(dates)
    factor = 60 * 60 * 24
    dates = np.divide(dates, factor)
    # dates = dates.tolist()
    pprint.pprint(dates)

    # print(type(dates))

    # newdates = matplotlib.dates.date2num(dates)
    # # Histogram with modified axes/grid

    fig = plt.figure()

    ax = fig.add_subplot(111, axisbg='#EEEEEE')
    ax.grid(color='white', linestyle='solid')
    bin = math.floor(dates[-1] - dates[0])
    print(bin)
    # ax.plot(dates, dates)

    
    
    ax.hist(dates, bin, histtype='stepfilled', fc='lightblue', alpha=0.5)
    ax.xaxis.set_major_locator( mdates.DayLocator() )
    ax.xaxis.set_major_formatter( mdates.DateFormatter('%Y-%m-%d') )
    ax.set_xticklabels(ax.xaxis.get_majorticklabels(), rotation=90)
    mpld3.show(fig)

    # r = newdates
    
    # fig, ax = plt.subplots(1)
    # ax.plot(dates, dates)
    # # fig.autofmt_xdate()
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y:%m:%d', tz=PST()))
    # mpld3.show(fig)


    # hfmt = matplotlib.dates.DateFormatter('%m %d %Y')
    
    # ax = fig.add_subplot(111, axisbg='#EEEEEE')
    # ax.grid(color='white', linestyle='solid')
    # ax.xaxis.set_major_locator(matplotlib.dates.MonthLocator())
    # ax.xaxis.set_major_formatter(hfmt)
    # ax.set_ylim(bottom=0)
    # ax.hist(newdates, 1000, histtype='stepfilled', fc='lightblue', alpha=0.5)
    # plt.xticks(rotation='vertical')
    # plt.subplots_adjust(bottom=.3)
    
    # pprint.pprint(mpld3.fig_to_dict(fig))
    # html = mpld3.fig_to_html(fig)

    # with open('plot_html.html', 'wb') as output:
    #     output.writelines(html)
    # mpld3.show(fig)

    # plt.plot([3, 1, 4, 1, 5], 'ks-', mec='w', mew=5, ms=20)
    # mpld3.show()
