from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import func


from .models import (
    DBSession,
    MyModel,
    )

import time
import pytz


def epoch_time(dt):
    """Method to convert datetime object into epoch time in days."""
    utc = pytz.timezone('UTC')
    utc_dt = utc.normalize(dt.astimezone(utc))
    return time.mktime(utc_dt.timetuple())/60/60/24


def convert_json(query):
    """Convert sqlalchemy query into JSON serializable list."""
    list_output = []
    for x in query:
        """Convert datetime into epoch_time."""
        x.__dict__['date_time'] = epoch_time(x.__dict__['date_time'])
        del x.__dict__['_sa_instance_state']
        list_output.append(x.__dict__)
    return list_output


@view_config(route_name='home', renderer='templates/test.jinja2')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.gid == 378).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'seattle'}


@view_config(route_name='one_hundred', renderer='templates/radius_test.jinja2')
def one_hundred(request):
    "Returns JSON object with list of dictionaries."
    try:
        output = DBSession.query(MyModel).filter(func.ST_Point_Inside_Circle(MyModel.the_geom, -122.336072, 47.623636, 0.001))
        # print 'query: {}\ncount: {}'.format(output, output.count())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    # Convert sqlalchemy object into list of dictionaries.
    return {'output': convert_json(output)}


@view_config(route_name='MVP', renderer='json')
def mvp(request):
    "Returns JSON object with all incidents from given lat/long within a set radius."
    lat = request.params.get('latitude', None)
    lon = request.params.get('longitude', None)
    try:
        output = DBSession.query(MyModel).filter(func.ST_Point_Inside_Circle(MyModel.the_geom, lon, lat, 0.001))
        # print 'query: {}\ncount: {}'.format(output, output.count())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # Convert sqlalchemy object into list of dictionaries.
    return {'output': convert_json(output)}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_seattle_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

