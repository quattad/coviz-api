import pytest

import pandas as pd
from pandas.testing import assert_frame_equal

import numpy as np
from numpy.testing import assert_array_equal

from utils.parse_csv_to_df import parse_dates, parse_countries, parse_cases
import time
from datetime import datetime, date

# Initialize test csv pat
test_csv = "tests\\unit\\test_utils\\test.csv"

""" parse_dates """
def test_parse_dates_read_correct_csv_path():
    # check if given a correct csv path, dataframe with dates is returned
    result = parse_dates(test_csv)
    
    expected_result = pd.DataFrame(["4/3/2020", "4/4/2020"], columns=["dates"])
    assert assert_frame_equal(left=result, right=expected_result) is None

# def test_parse_dates_read_incorrect_csv_path():
#     # test if given incorrect, correct error is thrown

""" parse_countries """

""" parse_cases for deaths """
def test_parse_cases_deaths_correct_csv_path():
    # test if given a correct csv path, dataframe with correct headers and data is returned
    result = parse_cases(test_csv, "deaths")
    
    expected_result = pd.DataFrame(
        {
            "dates": [datetime(2020, 4, 3), datetime(2020, 4, 4),datetime(2020, 4, 3), datetime(2020, 4, 4), datetime(2020, 4, 3), datetime(2020, 4, 4)], 
            "country_name": ["singapore", "singapore", "united_kingdom", "united_kingdom", "united_kingdom", "united_kingdom"],
            "province": ["", "", "bermuda", "bermuda", "cayman_islands", "cayman_islands"],
            "deaths": [123, 101112, 456, 131415, 789, 161718]
        },
        columns=["dates", "country_name", "province", "deaths"]
        )
    
    # convert both to numpy
    # tried using dataframe comparison but kept failing on column str comparison
    result.to_numpy()
    expected_result.to_numpy()
    
    assert assert_array_equal(x=result, y=expected_result) is None
    
""" parse_cases for confirmed """
def test_parse_cases_confirmed_correct_csv_path():
    # test if given a correct csv path, dataframe with correct headers and data is returned
    result = parse_cases(test_csv, "confirmed")

    expected_result = pd.DataFrame(
        {
            "dates": [datetime(2020, 4, 3), datetime(2020, 4, 4),datetime(2020, 4, 3), datetime(2020, 4, 4), datetime(2020, 4, 3), datetime(2020, 4, 4)], 
            "country_name": ["singapore", "singapore", "united_kingdom", "united_kingdom", "united_kingdom", "united_kingdom"],
            "province": ["", "", "bermuda", "bermuda", "cayman_islands", "cayman_islands"],
            "confirmed": [123, 101112, 456, 131415, 789, 161718]
        },
        columns=["dates", "country_name", "province", "confirmed"]
        )
    
    # convert both to numpy
    # tried using dataframe comparison but kept failing on column str comparison
    result.to_numpy()
    expected_result.to_numpy()
    
    assert assert_array_equal(x=result, y=expected_result) is None