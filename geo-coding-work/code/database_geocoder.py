import geopy
import pandas
import sqlite3
from geopy.geocoders import Nominatim

def geocode_data(database_name):

    geolocator = Nominatim(scheme='http',timeout=5)

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute('SELECT id, address, latitude, longitude FROM Address WHERE latitude IS NULL;')

    rows = cur.fetchall()

    for row in rows:

        id = row[0]
        address = str(row[1]) + ', Ann Arbor, MI'
        geolocation = geolocator.geocode(address)

        if geolocation is not None:
            sql = "UPDATE Address SET latitude = ?, longitude = ? WHERE id = ?;"
            val = (geolocation.latitude, geolocation.longitude, id)
            cur.execute(sql, val)
        else:
            sql = "UPDATE Address SET latitude = 0.0, longitude = 0.0 WHERE id = ?;"
            val = (id,)
            cur.execute(sql, val)

        conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__":

    database_name = "data.sqlite"
    table_name = "Address"

    geocode_data(database_name)
