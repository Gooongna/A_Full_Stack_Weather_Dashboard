import zipfile

def ftp2db(ftp, dir, conn, cursor, required_data, output):
    """
    ftp: ftp connection
    ftp_dir: dataset dir on ftp
    conn: db connection
    cursor: db cursor
    required_data: list
    output: output dir to store downloaded data
    """
    # forward to dataset dir
    ftp.cwd(dir) 

    # list directory filenames (reason: filename date != date info in given station_list)
    zip_files = []
    ftp.retrlines('NLST', zip_files.append) 

    zip_id = [zip_file_name[16:21] for zip_file_name in zip_files] # keep it as a list bcs to doing visualization, need to consider extenable requirement

    for id in required_data:
        if id in zip_id:
            zip_file_name = zip_files[zip_id.index(id)]

            # download zip from FTP to local
            ftp.retrbinary("RETR " + zip_file_name, open('{}/{}'.format(output, zip_file_name), 'wb').write) 

            # import only weather data to postgredb
            with zipfile.ZipFile('dataset/{}'.format(zip_file_name)) as zfile:
                # check if the zip contain the required weather file
                check = 0 
                # zip_file does not support to open wildcard 'produkt_*.txt' so use a loop
                for info in zfile.infolist():
                    weather_file_name = info.filename
                    if weather_file_name.startswith('produkt_tu_stunde'): 
                        check += 1

                        # db: create table
                        cursor.execute("""
                            CREATE TABLE temperature.{}(
                            STATIONS_ID INT,
                            MESS_DATUM VARCHAR(36),
                            QN_9 INT,
                            TT_TU FLOAT,
                            RF_TU FLOAT,
                            eor VARCHAR(36),
                            PRIMARY KEY (MESS_DATUM))
                        """.format(weather_file_name[:-4])) # aviod the '.txt' extension from weather file name

                        # db: import .txt
                        with zfile.open(weather_file_name, 'r') as f:
                            next(f) # Skip the header row.
                            cursor.copy_from(f, 'temperature.{}'.format(weather_file_name[:-4]), sep=';')
                            print('Successfully import: {} !'.format(weather_file_name[:-4]))

                if not check:
                    print("Not found: produkt_tu_stunde_*.txt in {}".format(zip_file_name))
        
        else:
            print("Not found: stundenwerte_TU_*_hist.zip for station {}".format(id))

    # commit all changes of db
    conn.commit() 