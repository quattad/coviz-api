from werkzeug.routing import BaseConverter
from datetime import datetime, date

class DateConverter(BaseConverter):
    def __init__(self):
        pass    
        
    def to_python(self, value):
        """ Takes in input of date string as format YYYY-MM-DD and converts to datetime object. 
        """
        date_string = value.split('-')
        return datetime(int(date_string[0]), int(date_string[1]), int(date_string[2])) 
        
    def to_url(self, value):
        """
        Take in input as a datetime object
        """
        timestamp_string = value.strftime("%Y-%m-%d")
        return timestamp_string