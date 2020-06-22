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
Filters for multiple queries
"""

import operator
from utils.custom_converters import DateConverter

class QueryValidationError(Exception):
    """ Handle exceptions and return HTTP response """
    pass

class Filter:
    # more information on supported filters - https://docs.python.org/3/library/operator.html
    supported_operators = ("eq", "ne", "lt", "le", "gt", "ge")
    
    def __init__(self, column, operator, value):
        self.column = column
        self.operator = operator
        self.value = value
    
    def validate(self):
        """ Checks if provided operator is supported """
        if operator not in self.supported_operators:
            raise QueryValidationError(
                f"operator `{operator}` is not one of supported operators `{self.supported_operators}`"
            )

def parse_value(column, value):
    dc = DateConverter()
    
    """ Parses the value into desired type based on column """
    if column == 'confirmed' or column == 'deaths' or column == 'recovered':
        return int(value)
    elif column == 'date':
        # parse datetime
        return dc.to_python(value)
    else:
        return value

def parse_filter(filter):
    # each filter is in the form (column, 'operator, value')
    # return list as [column, operator, value]
    column, op_val = filter[0], filter[1]
    
    # assume all values will be input since testing for cases only
    # if using filter query for other columns, need to parse for date
    op_val_split = op_val.split(",")
    
    # parse value
    
    return [column, op_val_split[0], parse_value(column, op_val_split[1])]
                
def create_filters(filters):
    """ 
    Process list filters into list of Filter objects 
    """
    filters_processed = []
    
    if not filters:
        # no filters provided
        return filters_processed
    
    elif len(filters) == 1:
        # check whether single filter
        # each filter is in the form (column, 'operator, value')
        filters_processed.append(
            Filter(*parse_filter(filters[0]))  # check why need to put pointer
        )
    
    elif isinstance(filters, list):
        # check whether multiple filters
        try:
            filters_processed = [Filter(*parse_filter(filter)) for filter in filters]
        except Exception:
            raise QueryValidationError("Invalid filter query")
    
    else:
        # filters are not str or list of str
        raise TypeError(
            f"filters expected to be `str` or `list` but was of type {type(filters)}"
        )
    
    return filters_processed

def filter_query(filters, query, model):
    """ 
    filters - list of Filter objects
    query - query object
    model - Model object used to obtain column from Model
    """
    for _filter in filters:
        # fetch operator from filter objects
        op = getattr(operator, _filter.operator)
        
        # fetch column from model
        column = getattr(model, _filter.column)
        
        # value for filter
        value = _filter.value
        
        # build up query by adding filters
        query = query.filter(op(column, value))
    
    return query