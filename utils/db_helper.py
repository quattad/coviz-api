# dict factory to specify formatting for sql results
import sqlite3

def dict_factory(cursor, row):
    d = {}
    
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        
    return d

def connect_to_db(db_path):
    """ Takes in database path as an argument and returns cursor after connecting """
    
    try:
        conn = sqlite3.connect(database="{}".format(db_path))
        print("Connection to db {} successful.".format(db_path))
    except Exception:
        print("Connection failed")
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    return cur