# Copyright 2920 Jonathan Quah. All Rights Reserved.
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

"""
Create and configure Flask app
Set up logging
Setup SQL database
"""
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_admin import Admin
import os
from utils.scheduler_update_csv_from_repo import scheduler
from utils.import_tables import import_tables_from_csv

# initialize extensions
db = SQLAlchemy()
admin = Admin(template_mode="bootstrap3")

app = Flask(__name__)

# import configurations
app.config.from_object('config.config.DevelopmentConfig')

# initialize api with Flask application. same as api.init_app(app)
api = Api(app)

# add converters
from utils.custom_converters import DateConverter
app.url_map.converters['date'] = DateConverter

from api import routes, models

# connect to db
try:
    routes.init_db()  # calls model init_db function to initialize db session
except Exception as error:
    app.logger.critical("{}: Cannot continue".format(error))

app.logger.info("Service initialized!")

# configure admin
if os.getenv("FLASK_ENV") == "development":
    admin.init_app(app)
    app.logger.info("Registered admin")

# shell context for Flask CLI
@app.shell_context_processor
def context():
    return {
        "app": app,
        "db": db
        }

# import tables from csv
import_tables_from_csv()

# initialize scheduler only in production
if os.getenv("FLASK_ENV") == "production":
    scheduler()