# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#    return 'Hello world'

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# The create_engine() function allows us to access and query our SQLite database file. 
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# create a variable for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link
session = Session(engine)

# create a Flask application called "app."
app = Flask(__name__)

# define the welcome route
@app.route("/")

# add the routing information for each of the other routes
# then, add precipitation, stations, tobs, and temp routes into return statement
def welcome():
        return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

 # create precip route
@app.route("/api/v1.0/precipitation")

# create precip function
# calculate the date one year ago from the most recent date in the database
# get the date and precipitation for the previous year
# ".\" signifies that we want our query to continue on the next line
# create (jsonify) a dictionary with the date as the key and the precipitation as the value

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# define station route and route name.
@app.route("/api/v1.0/stations")

# create a new function
# unravel results into a one-dimensional array and convert unraveled results into a list
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# define temperature observation route
@app.route("/api/v1.0/tobs")

# create a new tobs function
# calculate the date one year ago from the last date in the database
# query the primary station for all the temperature observations from the previous year.
# unravel the results into a one-dimensional array and convert that array into a list
# jsonify the list and return results
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# create statistics route, providing start and end date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create stats function
# add start and end parameters and set to none
# create a query to select the minimum, average, and maximum temperatures from SQLite database.
# Since we need to determine the starting and ending date, add "if-not" statement to the code
# query the database 
# unravel the results into a one-dimensional array and convert that array into a list
# jsonify the list and return results
# (*sel) indicates there will be multiple results for the query: min, avg, and max temps.
# sel list is the data points we need to collect
# calculate the temperature minimum, average, and maximum with the start and end dates
# query statistics data

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
    

