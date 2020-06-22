import pandas as pd
import pymysql
import sys

from sqlalchemy import create_engine, types

def csv_to_mysql(load_sql, host, user, password):
    try:
        con = pymysql.connect(
            host = host,
            user = user,
            password = password,
            autocommit = True,
            local_infile = 1  # grant permission to write to db from an input file
        )
        
        print("Connected to db: {}".format(host))
        
        # Create cursor
        cursor = con.cursor()
        cursor.execute(load_sql)
        con.close()
        
    except Exception as error:
        print("Error: {}".format(str(error)))
        sys.exit(1)