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
#  READ / GET / ID
######################################################################

def test_get_day_by_id_exists(test_app, test_database):
    """ Test if given valid input with entry already exist in database, response status code is 400 with correct error message """
    client = test_app.test_client()
    
    # add test user
    test_response = client.post('/v1/resources/time-series/api/countries',
                           data=json.dumps({
                               "country_name": "unique country",
                               "province": "test province 4",
                               "date": "2020-04-04",
                               "confirmed": 4,
                               "deaths": 3,
                               "recovered": 55
                               }),
                           content_type='application/json')
    
    test_data = json.loads(test_response.data.decode())
    id = test_data['id']

    client = test_app.test_client()
    response = client.get('/v1/resources/time-series/api/country/{}'.format(id))
    
    data = json.loads(response.data.decode())
    
    assert response.status_code == 200
    assert data['country_name'] == "unique country"
    assert data['province'] == "test province 4"
    assert data['date'] == "2020-04-04"
    assert data['confirmed'] == 4
    assert data['deaths'] == 3
    assert data['recovered'] == 55
    
