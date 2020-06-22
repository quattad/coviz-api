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

######################################################################
#  T E S T   C A S E S
######################################################################

######################################################################
#  CREATE
######################################################################

def test_add_days_valid_json(test_app, test_database):
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
    
    # decoding determined by content type
    # json.loads() - takes in string and returns json object
    # json.dumps() - takes in json object and returns string
    data = json.loads(response.data.decode())
    
    assert response.status_code == 201
    assert 'Location' in response.headers
    assert 'Message' in response.headers
    assert response.headers['Message'] == "day created"
    
######################################################################
#  READ
######################################################################

######################################################################
#  UPDATE
######################################################################

######################################################################
#  DELETE
######################################################################