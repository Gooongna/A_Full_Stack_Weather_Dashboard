import sys
import psycopg2
from flask import Flask, request, jsonify, render_template

import config
from data import dataCollection

app = Flask(__name__)

conn = psycopg2.connect(
        host=config.postgredb['host'], 
        port=config.postgredb['port'],
        dbname=config.postgredb['dbname'],
        user=config.postgredb['user'],
        password=sys.argv[1])
cursor = conn.cursor()
postgredb = dataCollection(conn, cursor)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        if request.form['go-button']== 'Go':
            city = request.form['city']
            linechartData = postgredb.get_christmas(city)
    else: # defualt city
        city = 'Heidelberg'
        linechartData = postgredb.get_christmas(city)

    return render_template(
        'dashboard.html', 
        city = city,
        lineDate = linechartData[0],
        lineData1 = linechartData[1],
        lineData2 = linechartData[2],
    )

if __name__ == "__main__":
    app.run(debug=True)