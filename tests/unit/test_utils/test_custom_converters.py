from utils.custom_converters import DateConverter
from datetime import date, datetime

""" DateConverter
"""
def test_date_converter_to_python_correct_str_to_datetime():
    
    dc = DateConverter()
    test_input = "1994-05-10"
    expected_result = datetime(1994, 5, 10)
    
    result = dc.to_python(test_input)
    
    assert result == expected_result
    assert type(result) == type(expected_result)
    
def test_date_converter_to_url_correct_datetime_to_str():
    
    dc = DateConverter()
    test_input = datetime(1994, 5, 10)
    expected_result = "1994-05-10"
    
    result = dc.to_url(test_input)
    
    assert result == expected_result
    assert type(result) == type(expected_result)
    
    