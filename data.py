import sys
import psycopg2
import pandas as pd
from geopy.geocoders import Nominatim
from math import radians, cos, sin, asin, sqrt

import config

class dataCollection:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
    
    def get_stations_list(self, table_name):
        """
        Retrieve the overview table of all selected 30 stations
        """
        self.cursor.execute("""
            SELECT * FROM station.{}
            """.format(table_name))
        result = self.cursor.fetchall()

        return result
        
    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points on the earth
        """
        # convert decimal degrees to radians 
        lat1, lon1, lat2, lon2  = map(radians, [lat1, lon1, lat2, lon2])

        # haversine formula 
        dlat = lat2 - lat1 
        dlon = lon2 - lon1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers

        return c * r
    
    def get_closest_station(self, input):
        """
        Compute the closest station by latitude and longitude
        """
        geolocator = Nominatim(user_agent='ChristmasWeather')
        input_location = geolocator.geocode(input)

        stations = self.get_stations_list('station_list')

        min_dis = 20000 # longest distance on earth - Rosario, Argentina to Xinghua, China: 19-20 km
        closest_station_id = 0
        for station in stations : 
            dis = self.haversine(input_location.latitude, input_location.longitude, station[4], station[5])
            if dis < min_dis:
                min_dis = dis
                closest_station_id = station[0]

        return str(closest_station_id).zfill(5)

    def get_table_name(self, station_id):
        """
        Get the full table name by station_id
        """
        self.cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'temperature' and table_name LIKE '%{}%'
        """.format(station_id))
        result = self.cursor.fetchone()[0]

        return result

    def get_christmas(self, input):

        """
        Compute the average  daily temperature and humidity for all christmases in the past
        """
        station_id = self.get_closest_station(input)
        weather_table_name = self.get_table_name(station_id)

        self.cursor.execute("""
            SELECT SUBSTR(mess_datum, 0, 9) AS datum, AVG(tt_tu), AVG(rf_tu)
            FROM temperature.{}
            WHERE mess_datum LIKE '%1225%'
            GROUP BY SUBSTR(mess_datum, 0, 9)
        """.format(weather_table_name))
        
        result = self.cursor.fetchall()
        result = list(map(list,zip(*result))) # list of 1st element in tuple, 2nd element in tuple

        result[1] = list(map(round, result[1]))
        result[2] = list(map(round, result[2]))

        return result    

if __name__ == "__main__":

    conn = psycopg2.connect(
        host=config.postgredb['host'], 
        port=config.postgredb['port'],
        dbname=config.postgredb['dbname'],
        user=config.postgredb['user'],
        password=sys.argv[1])
    cursor = conn.cursor()
    postgredb = dataCollection(conn, cursor)
    print(postgredb.get_christmas('Heidelberg'))