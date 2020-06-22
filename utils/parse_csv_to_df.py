# takes in timeseries csv file as input and returns df with col. headers corresponding to model
import csv
import pandas as pd
from collections import defaultdict

def parse_dates(csv_to_parse):
    # return df with dates only
    data = []
    
    with open(csv_to_parse) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        
        # assume in first row, first 4 columns (up to D) are headers
        # all other cels after that contain date range
        data = []
        
        for row in csv_reader:
            if line_count == 0:
                data = row[4:]
            
            line_count += 1
    
    df = pd.DataFrame(data, columns=["dates"])
    
    return df
        
def parse_countries(csv_to_parse):
    # return df with countries and states
    
    data = defaultdict(list)
    
    with open(csv_to_parse) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        
        for row in csv_reader:  # row read as {col1: value1, col2:value2, ...}
            for key, value in row.items():
                data[key].append(value)
        
    df = pd.DataFrame({
        "country_name" : data["Country/Region"], 
        "province": data["Province/State"]
        }, columns=["country_name", "province"])

    return df

def parse_cases(csv_to_parse, case_type):
    # applies to confirmed, deaths and recovered csv files
    # takes csv and case type (confirmed, deaths and recovered) and return df with dates, countries
    # and cases with header corresponding to header
    data = defaultdict(list)
    
    with open(csv_to_parse) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        
        for row in csv_reader:  # row read as {col1: value1, col2:value2, ...}
            
            curr_country = ""
            curr_province = ""
            
            for key, value in row.items():
                if key == "Country/Region" or key == "Province/State":
                    # no need to append to country/region here, add country_region only when date is added
                    if key == "Country/Region":
                        curr_country = value.lower().replace(' ', '_')
                    else:
                        curr_province = value.lower().replace(' ', '_')
                elif key == "Lat" or key == "Long":
                    continue
                else:
                    # header is a date, value are the cases
                    data["Dates"].append(pd.to_datetime(key))
                    data["Cases"].append(int(value))
                    
                    # add additional elements to Country/Region and Province lists
                    data["Country/Region"].append(curr_country)
                    data["Province/State"].append(curr_province)
    
    # order df
    df = pd.DataFrame(data, columns=["Dates", "Country/Region", "Province/State", "Cases"])
    
    # rename headers
    df.rename(columns=
              {
                "Dates": "dates", 
                "Country/Region": "country_name",
                "Province/State": "province", 
                "Cases": "{}".format(case_type)
            },
              inplace=True
            )
    
    return df