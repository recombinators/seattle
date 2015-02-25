from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    func
    )
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
    date_time = sa.Column(sa.DateTime, nullable=False)
    incident_type = sa.Column(sa.UnicodeText, nullable=False)
    address = sa.Column(sa.UnicodeText, nullable=False)
    incident_number = sa.Column(sa.UnicodeText, nullable=False)
    latitude = sa.Column(sa.UnicodeText, nullable=False)
    longitude = sa.Column(sa.UnicodeText, nullable=False)
    the_geom = sa.Column(sa.UnicodeText, nullable=False)

    @classmethod
    def by_gid(cls, gid):
        return DBSession.query(cls).filter(cls.gid == gid).one()

    @classmethod
    def by_incident_type(cls, incident_type):
        return DBSession.query(cls).filter(cls.incident_type == incident_type).all()

    @classmethod
    def circle_radius(cls, lat, lon, radius):
        return DBSession.query(cls).filter(func.ST_Point_Inside_Circle(cls.the_geom, lon, lat, radius)).all()

    def json(self):
        return {'gid': self.gid,
                'units': self.units,
                'date_time': self.date_time,
                'incident_type': self.incident_type,
                'address': self.address,
                'incident_number': self.incident_number,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'the_geom': self.the_geom}



# I don't know what this line is for:
Index('my_index', MyModel.gid, unique=True, mysql_length=255)
