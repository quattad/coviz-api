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
import os.path
from api import db
from config.config import TestingConfig
from api.models import GlobalTime

######################################################################
# Fixtures
######################################################################

"""
Benefits of fixtures
- explicit names and activated by declaring use from functions etc
- implemented in modular manner
- scales from simple unit testing to complex functional testing; allows fixtures/tests to be reusable
"""

# output failure test report 'failures'
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " ({})".format(item.funcargs["tmpdir"])
            else:
                extra = ""

            f.write(rep.nodeid + extra + "\n")
            
# create test app
@pytest.fixture(scope="function")
def test_app():
    from api import app
    app.config.from_object(TestingConfig)
    
    with app.app_context():
        yield app # testing

# create test db
@pytest.fixture(scope="function")
def test_database():
    db.create_all()
    yield db # testing
    
    # teardown
    db.session.remove()
    db.drop_all()

# create test GlobalTime days
@pytest.fixture(scope="function")
def define_add_test_day():
    def add_test_day(country_name, province, date, confirmed, deaths, recovered):
        day = GlobalTime(country_name=country_name, province=province, date=date, confirmed=confirmed, deaths=deaths, recovered=recovered)
        
        # add user to test db
        db.session.add(day)
        db.session.commit()
        
        return day
    
    return add_test_day