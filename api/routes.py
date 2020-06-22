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

"""
Also called views.py

Day

Paths:
------

Example:
GET /countries - Returns list of all the days
GET /country?name={country_name}&start_date={start_date}&end_date={end_date} - Returns days corresponding to country, start_date and end_date
"""

import os
import sys
import logging

from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status
from flask_restful import Resource, Api
from werkzeug.exceptions import NotFound # find out purpose
from utils.custom_converters import DateConverter
from datetime import timedelta

# import SQLAlchemy as ORM
from flask_sqlalchemy import SQLAlchemy
from api.models import GlobalTime, DataValidationError

# Import application
from api import app, api

# Test filter processing
from api.filters import Filter, create_filters, filter_query

@app.route("/", methods=["GET"])
def home():
    return {
        'test': 234
    }

######################################################################
# Error Handlers
######################################################################

@app.errorhandler(DataValidationError)
def request_validation_error(error):
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=message
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error="Not Found", message=message),
        status.HTTP_404_NOT_FOUND,
    )

@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=message,
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )

@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=message,
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=message,
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    
######################################################################
# GET INDEX
######################################################################
class Index(Resource):
    def get(self):
        """ Root URL response """
        return (
            jsonify(
                name="Coviz API",
                version="1.0",
                paths=url_for("cases_by_country_all")),  # how to reverse
            status.HTTP_200_OK
        )

######################################################################
# LIST ALL DAYS
######################################################################
class GetDaysByCountryNameAndDateRangeAPI(Resource):
    def get(self):
        """ Returns all days corresponding to args """
        app.logger.info("Returning all days")
        days = []  # store Query objects returned from db
        
        # get args from query params. date inputs must be YYYY-MM-DD
        country_name = request.args.get('country_name')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Generate list of Filter objects from query params
        filters = create_filters(list(request.args.items(multi=True)))

        # Get query object from model to query
        query = filter_query(filters, GlobalTime.query, GlobalTime)
        days = query.all()
                  
        result = [day.serialize() for day in days]
        return make_response(jsonify(result), status.HTTP_200_OK)
    
    def post(self):
        """
        Creates a day in the db 
        """
        check_content_type("application/json")
        
        # create Day instance
        day = GlobalTime()
        
        # check if any missing keys or invalid type
        try:
            day.deserialize(
                request.get_json()
            )
            
        except DataValidationError as error:
            abort(400, str(error))
            
        dc = DateConverter()
            
        check_country_name = day.country_name
        check_date = dc.to_url(day.date) # convert back to str
        
        res = GlobalTime.find_by_date_and_country_name(check_country_name, check_date)
        
        if res:
            abort(400, "Duplicate date for given country and date")
        
        app.logger.info("Creating day in db")
        day.create()
        
        # transform object into json
        day_json = day.serialize()

        # return of single day by searching for id
        location_url = url_for("get_day_by_id", day_id=day.id, _external=True)  # _external - generates absolute
        
        response = make_response(
            jsonify(day_json),
            status.HTTP_201_CREATED
        )
        
        # Attach custom headers to response.headers
        response.headers['Location'] = location_url
        response.headers['Message'] = "day created"
        
        return response
        
######################################################################
# GET DAY BY ID
######################################################################
class GetDayByIDAPI(Resource):
    """ 
    Get a day by ID
    """
    def get(self, day_id):
        app.logger.info("Request for day with id: {}".format(day_id))
        day = GlobalTime.find_by_id_or_404(day_id)
        
        if not day:
            raise NotFound("Day with id: '{}' was not found in the database.".format(day_id))
        
        return make_response(
            jsonify(day.serialize()), 
            status.HTTP_200_OK
            )
    
    def put(self, day_id):
        """ Update a day by ID """
        app.logger.info("Updating day entry with id: {}".format(day_id))
        day = GlobalTime.find_by_id_or_404(day_id)
        day.deserialize(request.get_json())
        day.id = day_id
        day.save()
        return make_response(
            jsonify(
                day.serialize(),
                status.HTTP_200_OK
            )
        )
        
    def delete(self, day_id):
        """ Update a day by ID """
        app.logger.info("Deleting day entry with id: {}".format(day_id))
        day = GlobalTime.find_by_id_or_404(day_id)
        day.delete()
        
        return make_response(
            "",
            status.HTTP_204_NO_CONTENT
        )


######################################################################
# GET DAY BY COUNTRY_NAME AND DATE
######################################################################
class GetDayByCountryNameAndDateAPI(Resource):
    """ Get day by specifying country name and date """
    def get(self):
        country_name = request.args.get('country_name')
        date_input = request.args.get('date')
        
        app.logger.info("Request for day with country_name: '{}' and date: '{}'".format(country_name, date_input))
        
        days = GlobalTime.find_by_date_and_country_name(country_name, date_input) # due to all() filter, will return list of dicts
        
        if not days:
            raise NotFound("Day with country_name: '{}' and date: '{}' was not found in the database".format(country_name, date_input))
        
        result = [day.serialize() for day in days]
        
        return make_response(
            jsonify(result),
            status.HTTP_200_OK
        )

######################################################################
# UPDATE DAYS
######################################################################


######################################################################
# DELETE DAYS
######################################################################

######################################################################
# CONSOLIDATED ENDPOINTS
######################################################################

api.add_resource(GetDaysByCountryNameAndDateRangeAPI, '/v1/resources/time-series/api/countries', endpoint='get_days_by_country_name_and_dates')
api.add_resource(GetDayByIDAPI, '/v1/resources/time-series/api/country/<int:day_id>', endpoint='get_day_by_id')
api.add_resource(GetDayByCountryNameAndDateAPI, '/v1/resources/time-series/api/country', endpoint='get_day_by_country_name_and_date')
# api.add_resource(CasesByCountryAndDateAPI, '/v1/resources/time-series/api/country', endpoint='cases_by_country_and_date')

######################################################################
# UTILITY FUNCTIONS
######################################################################

def init_db():
    """ Initialize SQLAlchemy app """
    global app
    GlobalTime.init_db(app)
    
def check_content_type(content_type):
    """ Check if request header is of required content type """
    if request.headers["Content-Type"] == content_type:
        app.logger.info("Request header of required content type: {}".format(content_type))
        return
    
    app.logger.error("Invalid content type: ".format(request.header["Content-Type"]))
    abort(415, "Content type should be: ".format(content_type))