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
#  READ / GET / COUNTRY_NAME & DATE
######################################################################

def test_get_day_by_country_name_and_date(test_app, test_database):
    """ Test if give valid parameters for country_name and date, response status code is 200 with correct fields """
    client = test_app.test_client()
    
    # add two dates for given location
    test_response_1 = client.post('/v1/resources/time-series/api/countries',
                        data=json.dumps({
                            "country_name": "singapura",
                            "province": "tampines",
                            "date": "2021-06-20",
                            "confirmed": 4,
                            "deaths": 3,
                            "recovered": 55
                            }),
                        content_type='application/json')
    
    test_data_1 = json.loads(test_response_1.data.decode())
    
    country_name = test_data_1['country_name']
    date = test_data_1['date']
    
    response = client.get('/v1/resources/time-series/api/country?country_name={}&date={}'.format(country_name, date))
    
    data = json.loads(response.data.decode())
    
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['country_name'] == "singapura"
    assert data[0]['province'] == "tampines"
    assert data[0]['date'] == "2021-06-20"
    assert data[0]['confirmed'] == 4
    assert data[0]['deaths'] == 3
    assert data[0]['recovered'] == 55