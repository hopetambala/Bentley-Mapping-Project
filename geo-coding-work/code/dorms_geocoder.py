import geopy
import pandas
import sqlite3
import re
from geopy.geocoders import Nominatim

def geocode_dorms(database_name):

    geolocator = Nominatim(scheme='http',timeout=5)

    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute('SELECT id, AddressNote, address, latitude, longitude FROM Address WHERE AddressNote = "dorm" AND latitude = 0.0;'),

    rows = cur.fetchall()

    for row in rows:

        id = row[0]

        line = row[2]
        pattern = "[[\w+\s]*\w+\s-]*|[\w+\s]*|[\w+\s\w+]*"

        match = re.findall(pattern, line)
        match = match[0].rstrip(" -")

        address = match + ', Ann Arbor, MI'

        geolocation = geolocator.geocode(address)

        if geolocation is not None:
            sql = "UPDATE Address SET latitude = ?, longitude = ? WHERE id = ?;"
            val = (geolocation.latitude, geolocation.longitude, id)
            cur.execute(sql, val)
        else:
            sql = "UPDATE Address SET address = ? WHERE id = ?;"
            val = (match, id)
            cur.execute(sql, val)

        conn.commit()

if __name__ == "__main__":

    database_name = "data.sqlite"
    table_name = "Address"

    geocode_dorms(database_name)
