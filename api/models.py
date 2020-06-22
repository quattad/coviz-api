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
Models for Coviz API

All of the models are stored in this module

Models
------
GlobalTime - A day of a particular country with confirmed, deaths and recovered cases of COVID-19

Attributes:
-----------
country_name (string) - name of country
province (string) - name of province/state
date (datetime) - date of particular day
confirmed (integer) - number of confirmed cases of COVID-19 on particular day
deaths (integer) - number of deaths due to COVID-19 on a particular day
recovered (integer) -  number of recoveries from COVID-19 on particular day

Class Methods:
-----------
Decorator @classmethod
Method that is bound to CLASS and not object of class
Able to modify class state that is applied to all instances of class
Takes 'cls' as the first parameter
Usually used to create factory methods (i.e. methods that return class object for different use cases)

EXAMPLE:
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    @classmethod
    def fromBirthYear(cls, name, year):
        return cls(name, date.today().year - year)
    
    ...

Static Methods:
-----------
Decorator @staticmethod

EXAMPLE:
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    @staticmethod
    def isAdult(age):
        return age > 18
    
    ...
"""

# Initialize db
from flask_sqlalchemy import SQLAlchemy
from api import app, db
import datetime
import logging
logger = logging.getLogger("flask.app")
from utils.custom_converters import DateConverter  # convert str to datetime object

class DataValidationError(Exception):
    """ 
    Used for data validation errors. 
    """
    pass

class GlobalTime(db.Model):
    """ 
    Class that represents a day of a particular country with confirmed, deaths and recovered cases of COVID-19
    """
    
    # Table schema
    id = db.Column(db.Integer, primary_key=True, unique=True)
    country_name = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(20))
    date = db.Column(db.DateTime, nullable=False)
    confirmed = db.Column(db.Integer, nullable=False)
    deaths = db.Column(db.Integer, nullable=False)
    recovered = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        """
        refers to how object is printed when its printed out
        """
        return "<GlobalTime object id={}, country_name={}, province={}, date={}, confirmed={}, deaths={}, recovered={}>".format(
            self.id, 
            self.country_name, 
            self.province, 
            self.date, 
            self.confirmed, 
            self.deaths, 
            self.recovered
        )
   
    # not required since deserialize function does the job of creating attributes for the object
    # def __init__(self, country_name, province, date, confirmed, deaths, recovered):
    #     """
    #     creation of object
    #     """
    #     self.country_name = country_name
    #     self.province = province
    #     self.date = date
    #     self.confirmed = confirmed
    #     self.deaths = deaths
    #     self.recovered = recovered
        
    def create(self):
        """
        Create globaltime 'day' in db
        """
        logger.info("Creating day with date={} for country={}, province={} with confirmed={}, deaths={}, recovered={}".format(self.date, self.country_name, self.province, self.confirmed, self.deaths, self.recovered))
        db.session.add(self)
        db.session.commit()
            
    def save(self):
        """ 
        Saves globaltime 'day' to db
        """
        logger.info("Saving day with date={} for country={}, province={} with confirmed={}, deaths={}, recovered={}".format(self.date, self.country_name, self.province, self.confirmed, self.deaths, self.recovered))
        db.session.commit()
        
    def delete(self):
        """
        Removes GlobalTime 'day' from db
        """
        logger.info("Removing day with date={} for country={}, province={} with confirmed={}, deaths={}, recovered={}".format(self.date, self.country_name, self.province, self.confirmed, self.deaths, self.recovered))
        db.session.delete(self)
        db.session.commit()
        
    def serialize(self):
        """
        Serializes GlobalTime 'day' from object into a dictionary 
        """
        dc =  DateConverter()
        return {
            "id":self.id,
            "country_name": self.country_name,
            "province": self.province,
            "date": dc.to_url(self.date),
            "confirmed": self.confirmed,
            "deaths": self.deaths,
            "recovered": self.recovered
        }
    
    def deserialize(self, data):
        """
        Deserializes GlobalTime 'day' from dictionary to object
        
        Args:
            data (dict): dictionary containing 'day' data
        """
        dc = DateConverter()
        
        try:
            self.country_name = data['country_name']
            self.province = data['province']
            self.date = dc.to_python(value=data['date'])
            self.confirmed = data['confirmed']
            self.deaths = data['deaths']
            self.recovered = data['recovered']
            
        except KeyError as error:
            raise DataValidationError("KeyError: Missing field '" + error.args[0] + "'")
        except TypeError as error:
            raise DataValidationError("TypeError: Body of request contained bad data")
        
        return self
    
    @classmethod
    def init_db(cls, app):
        """ Initialize database session """
        logger.info("Initializing database")
        cls.app = app
        
        # initialize SQLAlchemy from Flask app
        # will create .db file in directory that models.py is located in
        db.init_app(app)
        app.app_context().push()  # purpose?
        db.create_all()
        
    @classmethod
    def all(cls):
        """ Returns all 'days' in database """
        logger.info("Returning all days in database")
        return cls.query.all()
        
    @classmethod
    def find_by_id_or_404(cls, id):
        """ Return single day by id"""
        logger.info("Processing lookup for id={}".format(id))
        return cls.query.get_or_404(id)
        
    @classmethod
    def find_by_country_name(cls, country_name):
        """ Returns all days with given country_name """
        logger.info("Processing lookup for name={}".format(country_name))
        return cls.query.filter(cls.country_name == country_name)
        
    @classmethod
    def find_by_province(cls, province):
        """ Returns all days with given province """
        logger.info("Processing lookup for name={}".format(province))
        return cls.query.filter(cls.province == province)
        
    @classmethod
    def find_by_date(cls, date):
        """ Returns all days with given date """
        logger.info("Processing lookup for name={}".format(date))  # confirm how datetime should be parsed to string
        return cls.query.filter(cls.date == date)
    
    @classmethod
    def find_by_date_range(cls, start_date, end_date):
        """ Returns all days that fall within a date range by start date and end date """
        dc = DateConverter()
        logger.info("Processing lookup for days within range {} and {}".format(start_date, end_date))
        return cls.query.filter(cls.date.between(dc.to_python(value=start_date), dc.to_python(value=end_date)))
    
    @classmethod
    def find_by_date_and_country_name(cls, country_name, date):
        """ Returns one day that match given country name and date """
        dc = DateConverter()
        logger.info("Processing lookup for days with country_name: '{}' and date: '{}'".format(country_name, date))
        
        date_converted = dc.to_python(date)
        return cls.query.filter(cls.country_name == country_name, cls.date == date_converted).all()

    @classmethod
    def find_by_date_range_and_country_name(cls, country_name, start_date, end_date):
        """ Returns all days that fall within a date range by start date and end date """
        dc = DateConverter()
        logger.info("Processing lookup for days within range {} and {}".format(start_date, end_date))
        return cls.query.filter(cls.country_name == country_name, cls.date.between(dc.to_python(start_date), dc.to_python(end_date)))
    
    @classmethod
    def find_by_cases_confirmed(cls, confirmed):
        """ Returns all days given number of confirmed cases """
        logger.info("Processing lookup for confirmed cases={}".format(confirmed))
        return cls.query.filter(cls.confirmed == confirmed)
    
    @classmethod
    def find_by_cases_confirmed_range(cls, lower, upper):
        """ Returns all days given number of confirmed cases within lower and upper bound """
        logger.info("Processing lookup for confirmed cases between {} and {}".format(lower, upper))
        pass # to write query
        
    @classmethod
    def find_by_cases_deaths(cls, deaths):
        """ Returns all days given number of death cases """
        logger.info("Processing lookup for death cases={}".format(deaths))
        return cls.query.filter(cls.deaths == deaths)
    
    @classmethod
    def find_by_cases_deaths_range(cls, lower, upper):
        """ Returns all days given number of death cases within lower and upper bound """
        logger.info("Processing lookup for death cases between {} and {}".format(lower, upper))
        pass # to write query
        
    @classmethod
    def find_by_recovered(cls, recovered):
        """ Return all days by number of recovered cases """
        logger.info("Processing lookup for recovered cases={}".format(recovered))
        return cls.query.filter(cls.recovered == recovered)
    
    @classmethod
    def find_by_cases_recovered_range(cls, lower, upper):
        """ Returns all days given number of recovered cases within lower and upper bound """
        logger.info("Processing lookup for recovered cases between {} and {}".format(lower, upper))
        pass # to write query