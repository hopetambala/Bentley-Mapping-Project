import geopy
import pandas
import sqlite3
from numpy import nan
from geopy.geocoders import Nominatim

def import_data(filename):
    data = pandas.read_csv(filename, index_col=None, header=0, sep=",", encoding='latin-1')

    return data

def put_data_into_database(database_name, table_name, data):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    data.to_sql(table_name, conn, if_exists='append', index=False)

    conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":

    filename = "data/missing_latlong.csv"

    data = import_data(filename)

    database_name = "data.sqlite"
    table_name = "Address"

    put_data_into_database(database_name, table_name, data)

    print("Data imported successfully into database")
