import sys
import pandas as pd 
import psycopg2
from ftplib import FTP

import config
import ftp_to_db

# choose 30 stations from Baden-Württemberg to download
stations_df = pd.read_csv('dataset/station_list.csv', encoding = "ISO-8859-1")
stations_df['Stations_id'] = stations_df['Stations_id'].astype(str)
stations_df['Stations_id'] = stations_df['Stations_id'].apply(lambda x: x.zfill(5)) # add leading zero: 71 to 00071
stations_id = stations_df['Stations_id'].tolist()

# connect to FTP server
ftp = FTP('ftp-cdc.dwd.de')
ftp.login()

# connect to postgredb
conn = psycopg2.connect(
        host=config.postgredb['host'], 
        port=config.postgredb['port'],
        dbname=config.postgredb['dbname'],
        user=config.postgredb['user'],
        password=sys.argv[1])
cursor = conn.cursor()

# import data from FTP to postgredb
dir = 'climate_environment/CDC/observations_germany/climate/hourly/air_temperature/historical/'
ftp_to_db.ftp2db(ftp, dir, conn, cursor, stations_id, 'dataset')

# close cursor
cursor.close()