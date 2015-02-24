# from sqlalchemy import (
#     Column,
#     Index,
#     Integer,
#     Text,
#     )
import sqlalchemy as sa

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'incidents'
    gid = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    units = sa.Column(sa.UnicodeText, nullable=False)
    date_time = sa.Column(sa.UnicodeText, nullable=False)
    incident_type = sa.Column(sa.UnicodeText, nullable=False)
    address = sa.Column(sa.UnicodeText, nullable=False)
    incident_number = sa.Column(sa.UnicodeText, nullable=False)
    latitude = sa.Column(sa.UnicodeText, nullable=False)
    longitude = sa.Column(sa.UnicodeText, nullable=False)
    the_geom = sa.Column(sa.UnicodeText, nullable=False)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
