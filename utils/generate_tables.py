# from utils.csv_to_mysql import csv_to_mysql

import sqlite3

conn = sqlite3.connect("api/site.db")

c = conn.cursor()

# create "countries" table
# c.execute(""" --begin-sql
#           CREATE TABLE countries (
#               id integer PRIMARY KEY, 
#               dates_id integer NOT NULL, 
#               country_name text NOT NULL, 
#               province text,
#               FOREIGN KEY (dates_id) REFERENCES dates (id)
#               ) 
#               --end-sql""")

# create "dates" table
# c.execute(""" --begin-sql
#           CREATE TABLE dates (
#               id integer PRIMARY KEY, 
#               date text NOT NULL
#               ) 
#               --end-sql""")

# create "global_time" table
c.execute(""" --begin-sql
          CREATE TABLE global_time (
              id integer PRIMARY KEY,
              country_name text NOT NULL,
              province text,
              dates date NOT NULL, 
              deaths integer NOT NULL, 
              confirmed integer NOT NULL, 
              recovered integer NOT NULL) 
              --end-sql""")

# commit changes to the db
conn.commit()

# close connection to db
conn.close()