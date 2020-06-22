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
#  READ / GET
######################################################################

def test_get_day_by_date_range_exists(test_app, test_database):
    """ Test if given valid query parameters for country_name, start_date and end_date, response status code is 200 with correct error message """
    client = test_app.test_client()

    # add two dates for given location
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                        data=json.dumps({
                            "country_name": "singapura",
                            "province": "tampines",
                            "date": "2020-05-20",
                            "confirmed": 4,
                            "deaths": 3,
                            "recovered": 55
                            }),
                        content_type='application/json')
    
    test_response_2 = client.post('/v1/resources/time-series/api/countries',
                        data=json.dumps({
                            "country_name": "singapura",
                            "province": "tampines",
                            "date": "2020-05-23",
                            "confirmed": 62,
                            "deaths": 24,
                            "recovered": 24
                            }),
                        content_type='application/json')
    
    test_response_3 = client.post('/v1/resources/time-series/api/countries',
                    data=json.dumps({
                        "country_name": "singapura",
                        "province": "tampines",
                        "date": "2020-05-26",
                        "confirmed": 125,
                        "deaths": 235,
                        "recovered": 234
                        }),
                    content_type='application/json')
    
    test_data_1 = json.loads(test_response_1.data.decode())
    test_data_3 = json.loads(test_response_3.data.decode())
    start_date = test_data_1['date']
    end_date = test_data_3['date']
    
    response = client.get('/v1/resources/time-series/api/countries?date=ge,{}&date=le,{}'.format(start_date, end_date))
    data = json.loads(response.data.decode())
      
    # data will be returned as a list of dictionaries
    
    assert response.status_code == 200
    assert len(data) == 3
    
    # first set
    assert data[0]['country_name'] == "singapura"
    assert data[0]['province'] == "tampines"
    assert data[0]['date'] == "2020-05-20"
    assert data[0]['confirmed'] == 4
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55
    
    # second set
    assert data[1]['country_name'] == "singapura"
    assert data[1]['province'] == "tampines"
    assert data[1]['date'] == "2020-05-23"
    assert data[1]['confirmed'] == 62
    assert data[1]['deaths'] == 24
    assert data[1]['recovered'] == 24
    
    # third set
    assert data[2]['country_name'] == "singapura"
    assert data[2]['province'] == "tampines"
    assert data[2]['date'] == "2020-05-26"
    assert data[2]['confirmed'] == 125
    assert data[2]['deaths'] == 235
    assert data[2]['recovered'] == 234