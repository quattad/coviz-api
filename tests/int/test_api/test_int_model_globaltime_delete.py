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
#  DELETE
######################################################################

def test_delete_day_by_date_range_exists(test_app, test_database):
    """ Test if given day exists in the database, day is successfully deleted """
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
    
    test_data_1 = json.loads(test_response_1.data.decode())
    id_to_update = test_data_1['id']
    
    client.delete("/v1/resources/time-series/api/country/{}".format(id_to_update), content_type='application/json')
    
    response =  client.get("/v1/resources/time-series/api/country/{}".format(id_to_update), content_type='application/json')
    assert response.status_code == 404