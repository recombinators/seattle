from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .models import (
    DBSession,
    Incidents_Model,
    )

import time
import pytz
import math


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


# @view_config(route_name='center', renderer='json')
# def center(request):
#     "Returns lat/lon params"
#     lat = request.matchdict.get('lat', None)
#     lon = request.matchdict.get('lon', None)
#     try:
#         output = DBSession.query(Incidents_Model).filter(func.ST_Point_Inside_Circle(Incidents_Model.the_geom, lon, lat, 0.001))
#         # print 'query: {}\ncount: {}'.format(output, output.count())
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     # Convert sqlalchemy object into list of dictionaries.
#     return {'output': convert_json(output)}


@view_config(route_name='index', renderer='templates/index.jinja2')
def line_plot(request):
    "Returns epoch datetime params as a list."
    lat = 47.623636
    lon = -122.336072
    radius = 0.003
    try:
        output = []
        start_time = time.time()
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Fire', radius)))
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'MVI', radius)))
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Crime', radius)))
        print 'time to call db for initial query: {}'.format(time.time()-start_time)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    names = ['fire', 'mvi', 'crime'] #, 'other'
    output_dict = dict(zip(names, output))
    output_percentages = []
    output_percentages.append(Incidents_Model.percentage(output[0]))
    output_percentages.append(Incidents_Model.percentage(output[1]))
    output_percentages.append(Incidents_Model.percentage(output[2]))
    output_percentages_dict = dict(zip(names, output_percentages))

    min_date = min(min(output[0]), min(output[1]), min(output[2]))
    max_date = max(max(output[0]), max(output[1]), max(output[2]))
    date_range = max_date - min_date
    number_months = int(math.ceil(date_range/30))
    days_in_month = 30
    start_date = min_date
    date = start_date

    months = []
    for i in range(number_months):
        months.append(date)
        date += days_in_month
    # print(wks)

    count = [[0] * (number_months - 1), [0] * (number_months - 1), [0] * (number_months - 1)]
    for k in range(2):
        for i in output[k]:
            for j in range(number_months - 1):
                if i > months[j] and i < months[j+1]:
                    count[k][j] += 1
    print(count)

    return {'output': [months[1:], count],
            'percentages': output_percentages_dict}


@view_config(route_name='index_lat_long', renderer='templates/index.jinja2')
def line_plot_lat_long(request):
    "Returns epoch datetime params as a list."
    lat = 47.623636
    lon = -122.336072
    radius = 0.003
    try:
        output = []
        start_time = time.time()
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Fire', radius)))
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'MVI', radius)))
        output.append(epoch_list(Incidents_Model.cat_circle(lat, lon, 'Crime', radius)))
        print 'time to call db for initial query: {}'.format(time.time()-start_time)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    names = ['fire', 'mvi', 'crime'] #, 'other'
    output_dict = dict(zip(names, output))
    output_percentages = []
    output_percentages.append(Incidents_Model.percentage(output[0]))
    output_percentages.append(Incidents_Model.percentage(output[1]))
    output_percentages.append(Incidents_Model.percentage(output[2]))
    output_percentages_dict = dict(zip(names, output_percentages))

    min_date = min(min(output[0]), min(output[1]), min(output[2]))
    max_date = max(max(output[0]), max(output[1]), max(output[2]))
    date_range = max_date - min_date
    number_months = int(math.ceil(date_range/30))
    days_in_month = 30
    start_date = min_date
    date = start_date

    months = []
    for i in range(number_months):
        months.append(date)
        date += days_in_month
    # print(wks)

    count = [[0] * (number_months - 1), [0] * (number_months - 1), [0] * (number_months - 1)]
    for k in range(2):
        for i in output[k]:
            for j in range(number_months - 1):
                if i > months[j] and i < months[j+1]:
                    count[k][j] += 1
    print(count)

    return {'output': [months[1:], count],
            'percentages': output_percentages_dict}


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
