import pandas as pd
import os
import functools

from utils.parse_csv_to_df import parse_cases
from sqlalchemy import create_engine

def import_tables_from_csv():
    print("Importing time series csv into database...")
    """ Imports time series covid files into current db"""
    # find latest file in COVID-19 folder
    path = "data/COVID-19/csse_covid_19_data/csse_covid_19_time_series"

    # create connection to database using SQLAlchemy
    # will use env var unless running straight from terminal, then attach to dev db
    engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///api/site.db"), echo=False)

    # return latest csv file in folder
    csv_path_confirmed = path + "/time_series_covid19_confirmed_global.csv"
    csv_path_deaths = path + "/time_series_covid19_deaths_global.csv"
    csv_path_recovered = path + "/time_series_covid19_recovered_global.csv"
    files = [(csv_path_confirmed, "confirmed"), (csv_path_deaths, "deaths"), (csv_path_recovered, "recovered")]

    # obtain dataframes
    frames = [parse_cases(f[0], f[1]) for f in files]

    df_global_time = functools.reduce(lambda left, right: pd.merge(left, right, on=["dates", "country_name", "province"], how="inner"), frames)
    df_global_time.rename(columns={"dates":'date'}, inplace=True)

    # load df into db
    df_global_time.to_sql("global_time", con=engine, if_exists='append', chunksize=1000, index=False)
    
    print("Import complete.")