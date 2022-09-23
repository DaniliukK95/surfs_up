#9.5.1
#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#add SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#add dependencies for flask
from flask import Flask, jsonify

#set up the database engine
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database into our classes
Base = automap_base()

#reflect the tables
Base.prepare(engine, reflect=True)

#save our references to each table. give each class a variable
Measurement = Base.classes.measurement
Station = Base.classes.station

#create session link from python to our database
session = Session(engine)

#define our flask app. create flask app called app
app = Flask(__name__)

#define the welcome route
@app.route("/")
def welcome():
    return(
    "Welcome to the Climate Analysis API! <br/>"
    "Available Routes: <br/>"
    "/api/v1.0/precipitation <br/>"
    "/api/v1.0/stations <br/>"
    "/api/v1.0/tobs <br/>"
    "/api/v1.0/temp/start/end <br/>"
    )


#route for precipitation analysis
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)


#route for stations
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


#route for temperature observations
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


#route for statistics 
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
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