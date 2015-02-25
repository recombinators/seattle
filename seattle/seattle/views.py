from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy import func


from .models import (
    DBSession,
    Incidents_Model,
    )

import time
import pytz
import datetime


def epoch_time(dt):
    """Method to convert datetime object into epoch time in days."""
    utc = pytz.timezone('UTC')
    utc_dt = utc.normalize(dt.astimezone(utc))
    return time.mktime(utc_dt.timetuple())/60/60/24


def epoch_list(a_list):
    """Convert query.all() list into a sorted list with only epoch time."""
    date_list = []
    for item in a_list:
        date_list.append(epoch_time(item.date_time))

    return sorted(date_list)


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
        one = DBSession.query(Incidents_Model).filter(Incidents_Model.gid == 378).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'seattle'}


@view_config(route_name='MVP', renderer='json')
def mvp(request):
    "Returns JSON object with all incidents from given lat/long within a set radius."
    lat = request.params.get('latitude', None)
    lon = request.params.get('longitude', None)
    try:
        output = DBSession.query(Incidents_Model).filter(func.ST_Point_Inside_Circle(Incidents_Model.the_geom, lon, lat, 0.001))
        # print 'query: {}\ncount: {}'.format(output, output.count())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # Convert sqlalchemy object into list of dictionaries.
    return {'output': convert_json(output)}


@view_config(route_name='center', renderer='json')
def center(request):
    "Returns lat/lon params"
    lat = request.matchdict.get('lat', None)
    lon = request.matchdict.get('lon', None)
    try:
        output = DBSession.query(Incidents_Model).filter(func.ST_Point_Inside_Circle(Incidents_Model.the_geom, lon, lat, 0.001))
        # print 'query: {}\ncount: {}'.format(output, output.count())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    # Convert sqlalchemy object into list of dictionaries.
    return {'output': convert_json(output)}


@view_config(route_name='major_category',
             renderer='templates/test_cat.jinja2')
def major_cat(request):
    """Returns epoch datetime params as a dict with keys for each major type and
    values corresponding to the epoch times."""
    lat = 47.609907
    lon = -122.337779
    radius = 0.005
    try:
        output = []
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Fire', radius)))
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'MVI', radius)))
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Crime', radius)))
        # output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Other', radius)))
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    names = ['fire', 'mvi', 'crime'] #, 'other'
    output_dict = dict(zip(names, output))
    output_percentages = []
    output_percentages.append(Incidents_Model.percentage(output[0]))
    output_percentages.append(Incidents_Model.percentage(output[1]))
    output_percentages.append(Incidents_Model.percentage(output[2]))
    output_percentages_dict = dict(zip(names, output_percentages))


    return {'lists': output_dict, 'percentages': output_percentages_dict}




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

