# tutorial taken from: https://programminghistorian.org/lessons/mapping-with-python-leaflet

import geopy
import pandas
import sqlite3
from numpy import nan
from geopy.geocoders import Nominatim, GoogleV3
# versions used: geopy 1.10.0, pandas 0.16.2, python 2.7.8

def main():
  io = pandas.read_csv('data/missing_latlong.csv', index_col=None, header=0, sep=",", encoding='latin-1')

  def get_latitude(x):
    try:
        return x.latitude
    except:
        return 0.0

  def get_longitude(x):
    try:
        return x.longitude
    except:
        return 0.0

# Ask Dan
  geolocator = Nominatim(scheme='http',timeout=3)
  # returning geojson data:

  # API_KEY = 'AIzaSyCkD6eVmvS1WL5ZmemfgnGHVXuWGdiaccQ'
  # geolocator = GoogleV3(api_key=API_KEY, domain='maps.googleapis.com', scheme='https', client_id=None, secret_key=None, timeout=1, proxies=None)
  # uncomment the geolocator you want to use
  # print (io.head())
  io['address'] = io['address'].astype(str) + ', Ann Arbor, MI'
  geolocate_column = io['address'].apply(geolocator.geocode)

  io['latitude'] = geolocate_column.apply(get_latitude)
  io['longitude'] = geolocate_column.apply(get_longitude)
  io.to_csv('geocode_output.csv')

if __name__ == '__main__':
  main()
# geolocate_column.fillna(value='.', inplace=True)
# io["latitude"] = " "
# io["longitude"] = " "
# # print (geolocate_column)
# for index, row in geolocate_column.iteritems():
#     if not geolocate_column[[index]].Address=='.':
#       io[[index]].latitude = geolocate_column[[index]].apply(get_latitude)
#       io[[index]].longitude = geolocate_column[[index]].apply(get_longitude)



# # once we get CSV file from Bentley, create a function main() that reads your input CSV.
# def main():
#     io = pandas.read_csv('census.csv', index_col=None, header=0, sep=",")
#
#     def get_latitude(x):
#         return x.latitude
#
#     def get_longitude(x):
#         return x.longitude
#
#     geolocator = GoogleV3() # GoogleV3 is a reliable geolocator choice because of their large geographic data coverage and generous quotas
#
#     # Make sure columns from Bentley have consistent formatting when it comes to address data
#     geolocate_column = io['Area_Name'].apply(geolocator.geocode)
#     io['latitude'] = geolocate_column.apply(get_latitude)
#     io['longitude'] = geolocate_column.apply(get_longitude)
#     io.to_csv('test_census_data.csv') # outputs new columns into new CSV spreadsheet separate from original
#
# if __name__ == '__main__':
#   main()
