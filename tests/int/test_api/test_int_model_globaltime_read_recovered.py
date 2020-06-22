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

def test_get_day_by_recovered_1oo1(test_app, test_database):
    pass

def test_get_day_by_recovered_1oo2(test_app, test_database):
    pass

def test_get_day_by_recovered_2oo2(test_app, test_database):
    pass

def test_get_day_by_recovered_range_exists_1oo1(test_app, test_database):
    pass

def test_get_day_by_recovered_range_exists_1oo2(test_app, test_database):
    pass

def test_get_day_by_recovered_range_exists_2oo2(test_app, test_database):
    pass

def test_get_day_by_recovered_range_exists(test_app, test_database):
    pass

def test_get_day_by_recovered_range_lower_greater_than_upper(test_app, test_database):
    """ Test if lower range is greater than higher range, response status code is 400 with correct error message  """
    pass