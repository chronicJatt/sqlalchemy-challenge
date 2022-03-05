#################################################
# Import Dependencies
#################################################
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# Reflect database & tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
# Create app
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Home route
@app.route('/')
def welcome():
    return '''<html>
                <h1>Hawaii Climate API</h1>
                <hr>
                <p><a href='/api/v1.0/precipitation'>Precipitation Data for Last Year in Database</a></p>
                <p><a href='/api/v1.0/stations'>List of Stations and Station Names</a></p>
                <p><a href='/api/v1.0/tobs'>Temperature Data for Most Active Station (USC00519281)</a></p>
                <p>For custom queries, all dates must be entered in format YYYY-MM-DD.<br>
                Queries return minimum, average & maximum observed temperatures. In that order.</p>
                <p>Start Day Only Custom Query: <a href='/api/v1.0/<start>'>/api/v1.0/start_date</a></p>
                <p>Start & End Day Custom Query: <a href='/api/v1.0/<start>/<end>'>/api/v1.0/start_date/end_date</a></p>
            </html>'''

# Precipitation Route
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Perform a query to retrieve the data and precipitation scores
    prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23")
    # Convert into dictionary
    prcp_dict = dict(prcp)
    # JSONify dictionary
    return jsonify(prcp_dict)

# Stations Route
@app.route('/api/v1.0/stations')
def stations():
    # Query stations in database
    stations = session.query(Station.station, Station.name).all()
    # Convert stations query into list
    stations_list = list(np.ravel(stations))
    # JSONify stations list
    return jsonify(stations_list)

# Tobs Route
@app.route('/api/v1.0/tobs')
def tobs():
    # Query the most active station for last year of data
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= "2016-08-23").all()
    # Convert tobs query into list
    tobs_list = list(np.ravel(tobs))
    # JSONify tobs list
    return jsonify(tobs_list)

# Start Day Route
@app.route('/api/v1.0/<start>')
def start_day(start):
    start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    # Generate list
    start_day_list = list(np.ravel(start_day))
    # JSONify start day list
    return jsonify(start_day_list)


# Start/end Day Route
@app.route('/api/v1.0/<start>/<end>')
def start_end_day(start, end):
    start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    # Generate list
    start_end_day_list = list(np.ravel(start_end_day))
    # JSONify start/end day list
    return jsonify(start_end_day_list)

if __name__ == '__main__':
    app.run(debug=True)