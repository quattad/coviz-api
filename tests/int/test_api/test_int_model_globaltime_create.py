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
#  CREATE
######################################################################

def test_add_days(test_app, test_database):
    """ Test if given input with valid keys and values, entry is successfully created in db"""

    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "test country 5",
                               "province": "test province 4",
                               "date": "2020-04-04",
                               "confirmed": 1,
                               "deaths": 2,
                               "recovered": 3
                               }),
                           content_type='application/json')

    data = json.loads(response.data.decode())
    
    assert response.status_code == 201
    assert 'Location' in response.headers
    assert 'Message' in response.headers
    assert response.headers['Message'] == "day created"

def test_add_days_invalid_json(test_app, test_database):
    """ Test if given input with valid keys and values, entry is successfully created in db"""
    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({}),
                            content_type='application/json')
    
    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())
    
    assert response.status_code == 400
    assert data['message'] == "KeyError: Missing field 'country_name'"

def test_add_days_invalid_json_keys_missing_country_name(test_app, test_database):
    """ Test if given input with missing key: country_name, response status code is 400 with correct error message """
    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({
                                "province": "test province 4",
                                "date": "2020-04-04",
                                "confirmed": 1,
                                "deaths": 2,
                                "recovered": 3
                                }),
                            content_type='application/json')

    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['message'] == "KeyError: Missing field 'country_name'"
    
def test_add_days_invalid_json_keys_missing_date(test_app, test_database):
    """ Test if given input with missing key: date, response status code is 400 with correct error message """
    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({
                                "country_name": "test country 5",
                                "province": "test province 4",
                                "confirmed": 1,
                                "deaths": 2,
                                "recovered": 3
                                }),
                            content_type='application/json')

    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['message'] == "KeyError: Missing field 'date'"
    
def test_add_days_invalid_json_keys_missing_confirmed(test_app, test_database):
    """ Test if given input with missing key: confirmed, response status code is 400 with correct error message """
    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({
                                "country_name": "test country 5",
                                "province": "test province 4",
                                "date": "2020-04-04",
                                "deaths": 2,
                                "recovered": 3
                                }),
                            content_type='application/json')

    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['message'] == "KeyError: Missing field 'confirmed'"
    
def test_add_days_invalid_json_keys_missing_deaths(test_app, test_database):
    """ Test if given input with missing key: deaths, response status code is 400 with correct error message """
    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({
                                "country_name": "test country 5",
                                "province": "test province 4",
                                "date": "2020-04-04",
                                "confirmed": 4,
                                "recovered": 3
                                }),
                            content_type='application/json')

    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['message'] == "KeyError: Missing field 'deaths'"

def test_add_days_invalid_json_keys_missing_recovered(test_app, test_database):
    """ Test if given input with missing key: recovered, response status code is 400 with correct error message """
    client = test_app.test_client()   
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({
                                "country_name": "test country 5",
                                "province": "test province 4",
                                "date": "2020-04-04",
                                "confirmed": 4,
                                "deaths": 3
                                }),
                            content_type='application/json')

    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['message'] == "KeyError: Missing field 'recovered'"
    
def test_add_days_duplicate_entry(test_app, test_database):
    """ Test if given valid input with entry already exist in database, response status code is 400 with correct error message """
    client = test_app.test_client()
    
    response = client.post('/v1/resources/time-series/api/countries',
                        data=json.dumps({
                            "country_name": "unique country",
                            "province": "test province 4",
                            "date": "2020-04-04",
                            "confirmed": 4,
                            "deaths": 3,
                            "recovered": 55
                            }),
                        content_type='application/json')
        
    response = client.post('/v1/resources/time-series/api/countries',
                            data=json.dumps({
                                "country_name": "unique country",
                                "province": "test province 4",
                                "date": "2020-04-04",
                                "confirmed": 4,
                                "deaths": 3,
                                "recovered": 55
                                }),
                            content_type='application/json')

    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())

    assert response.status_code == 400
    assert data['message'] == "Duplicate date for given country and date"