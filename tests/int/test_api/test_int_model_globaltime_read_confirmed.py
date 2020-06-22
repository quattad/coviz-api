# Copyright 2020 Jonathan Quah. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import json
from datetime import datetime

from api import routes
from api.models import GlobalTime

######################################################################
#  T E S T   C A S E S
######################################################################

######################################################################
#  READ / GET / CONFIRMED
######################################################################

def test_get_day_by_confirmed_exists_single_day_1oo1(test_app, test_database):
    """ Test if given 1 day out of 1 meets number of confirmed cases, response status code is 200  """
    client = test_app.test_client()
    
    # add test user
    test_response = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "singapura",
                               "province": "tampines",
                               "date": "2020-05-10",
                               "confirmed": 4,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json')    
    
    test_data = json.loads(test_response.data.decode())
    confirmed = test_data['confirmed']

    response = client.get('/v1/resources/time-series/api/countries?confirmed=eq,{}'.format(confirmed))
    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    
    assert response.status_code == 200
    assert data[0]['country_name'] == "singapura"
    assert data[0]['province'] == "tampines"
    assert data[0]['date'] == "2020-05-10"
    assert data[0]['confirmed'] == 4
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55

def test_get_day_by_confirmed_exists_single_day_1oo2(test_app, test_database):
    """ Test if given 1 day out of 2 meets number of confirmed cases, response status code is 200  """
    client = test_app.test_client()
    
    # add test user
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "malaysia",
                               "province": "johor_bahru",
                               "date": "2027-05-10",
                               "confirmed": 1,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json')
    
    test_response_2 = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "singapura",
                               "province": "tampines",
                               "date": "2020-05-10",
                               "confirmed": 4,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json') 
    
    test_data = json.loads(test_response_1.data.decode())
    confirmed = test_data['confirmed']

    response = client.get('/v1/resources/time-series/api/countries?confirmed=eq,{}'.format(confirmed))
    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    
    assert response.status_code == 200
    assert data[0]['country_name'] == "malaysia"
    assert data[0]['province'] == "johor_bahru"
    assert data[0]['date'] == "2027-05-10"
    assert data[0]['confirmed'] == 1
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55
    
def test_get_day_by_confirmed_exists_single_day_2oo2(test_app, test_database):
    """ Test if given 2 days out of 2 meets number of confirmed cases, response status code is 200  """
    
    client = test_app.test_client()
    
    # add test user
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "malaysia",
                               "province": "johor_bahru",
                               "date": "2020-05-10",
                               "confirmed": 1021,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json')
    
    test_response_2 = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "singapura",
                               "province": "tampines",
                               "date": "2020-05-14",
                               "confirmed": 1021,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json') 
    
    test_data = json.loads(test_response_1.data.decode())
    confirmed = test_data['confirmed']

    response = client.get('/v1/resources/time-series/api/countries?confirmed=eq,{}'.format(confirmed))
    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    
    assert response.status_code == 200
    assert len(data) == 2
    
    assert data[0]['country_name'] == "malaysia"
    assert data[0]['province'] == "johor_bahru"
    assert data[0]['date'] == "2020-05-10"
    assert data[0]['confirmed'] == 1021
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55
    
    assert data[1]['country_name'] == "singapura"
    assert data[1]['province'] == "tampines"
    assert data[1]['date'] == "2020-05-14"
    assert data[1]['confirmed'] == 1021
    assert data[1]['deaths'] == 3
    assert data[1]['recovered'] == 55

def test_get_day_by_confirmed_range_exists_1oo1(test_app, test_database):
    """ Test if given 1 day out of 1 meets range of confirmed cases, response status code is 200  """

    client = test_app.test_client()
    
    # add test user
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "malaysia",
                               "province": "johor_bahru",
                               "date": "2025-05-10",
                               "confirmed": 1074,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json')
    
    lower_range = 1000
    upper_range = 1500

    response = client.get('/v1/resources/time-series/api/countries?confirmed=ge,{}&confirmed=le,{}'.format(lower_range, upper_range))
    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    
    assert response.status_code == 200
    assert len(data) == 1
    
    assert data[0]['country_name'] == "malaysia"
    assert data[0]['province'] == "johor_bahru"
    assert data[0]['date'] == "2025-05-10"
    assert data[0]['confirmed'] == 1074
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55

def test_get_day_by_confirmed_range_exists_1oo2(test_app, test_database):
    """ Test if given 1 day out of 2 meets range of confirmed cases, response status code is 200 """
     
    client = test_app.test_client()
    
    # add test user
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                                data=json.dumps({
                                    "country_name": "malaysia",
                                    "province": "johor_bahru",
                                    "date": "2020-05-10",
                                    "confirmed": 800,
                                    "deaths": 3,
                                    "recovered": 55
                                    }),
                                content_type='application/json')
    
    test_response_2 = client.post('/v1/resources/time-series/api/countries',
                                data=json.dumps({
                                    "country_name": "singapura",
                                    "province": "tampines",
                                    "date": "2020-05-14",
                                    "confirmed": 1021,
                                    "deaths": 3,
                                    "recovered": 55
                                    }),
                                content_type='application/json') 
    
    test_data = json.loads(test_response_1.data.decode())
    confirmed = test_data['confirmed']

    lower_range = 800
    upper_range = 1500

    response = client.get('/v1/resources/time-series/api/countries?confirmed=gt,{}&confirmed=lt,{}'.format(lower_range, upper_range))

    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    assert response.status_code == 200
    assert len(data) == 1
    
    assert data[0]['country_name'] == "singapura"
    assert data[0]['province'] == "tampines"
    assert data[0]['date'] == "2020-05-14"
    assert data[0]['confirmed'] == 1021
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55

def test_get_day_by_confirmed_range_exists_2oo2(test_app, test_database):
    """ Test if given 2 days out of 2 meets range of confirmed cases, response status code is 200  """

    client = test_app.test_client()
    
    # add test user
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                                data=json.dumps({
                                    "country_name": "australia",
                                    "province": "melbourne",
                                    "date": "2025-05-10",
                                    "confirmed": 124,
                                    "deaths": 3,
                                    "recovered": 55
                                    }),
                                content_type='application/json')
    
    test_response_2 = client.post('/v1/resources/time-series/api/countries',
                                data=json.dumps({
                                    "country_name": "australia",
                                    "province": "sydney",
                                    "date": "2023-05-11",
                                    "confirmed": 252,
                                    "deaths": 3,
                                    "recovered": 55
                                    }),
                                content_type='application/json') 
    
    test_data = json.loads(test_response_1.data.decode())
    confirmed = test_data['confirmed']

    lower_range = 100
    upper_range = 300

    response = client.get('/v1/resources/time-series/api/countries?confirmed=gt,{}&confirmed=lt,{}'.format(lower_range, upper_range))

    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    assert response.status_code == 200
    assert len(data) == 2
    
    assert data[0]['country_name'] == "australia"
    assert data[0]['province'] == "melbourne"
    assert data[0]['date'] == "2025-05-10"
    assert data[0]['confirmed'] == 124
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55
    
    assert data[1]['country_name'] == "australia"
    assert data[1]['province'] == "sydney"
    assert data[1]['date'] == "2023-05-11"
    assert data[1]['confirmed'] == 252
    assert data[1]['deaths'] == 3
    assert data[1]['recovered'] == 55

def test_get_day_by_confirmed_range_lower_greater_than_upper(test_app, test_database):
    """ Test if lower range is greater than higher range, response status code is 200 but return empty list  """
    client = test_app.test_client()
    
    # add test user
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "malaysia",
                               "province": "johor_bahru",
                               "date": "2020-05-10",
                               "confirmed": 1021,
                               "deaths": 35,
                               "recovered": 551
                               }),
                           content_type='application/json')
    
    lower_range = 1000
    upper_range = 1500

    response = client.get('/v1/resources/time-series/api/countries?confirmed=gt,{}&confirmed=lt,{}'.format(upper_range, lower_range))
    data = json.loads(response.data.decode())
    
    # data will be returned as a list of dictionaries
    assert response.status_code == 200
    assert len(data) == 0
    assert data == []