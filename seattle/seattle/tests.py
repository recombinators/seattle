#from contextlib import closing
#import unittest
#import transaction

#from pyramid_sqlalchemy.testing import DatabaseTestCase
#from pyramid import testing

# USE THIS FOR TESTING
# py.test tests.py --sql-url=postgresql://Joel:@localhost/seattle_test --sql-echo -s

from models import DBSession, Incidents_Model, Neighborhoods_Model
from views import line_plot, line_plot_lat_long_ajax

import pytest


TEST_DSN = 'dbname=seattle_test user=Joel'

# NEIGHBORHOOD TESTS
def test_neighborhood_returns_correctly(sql_session):
    neighborhood = Neighborhoods_Model.neighborhood(47.6770046, -122.3849916,
                                                    sql_session)
    assert neighborhood == 'Loyal Heights'


def test_neighborhood2_returns_correctly(sql_session):
    neighborhood = Neighborhoods_Model.neighborhood(47.698, -122.302,
                                                    sql_session)
    assert neighborhood == 'Meadowbrook'



