#import dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from flask import Flask, jsonify

#create SQL connection / session
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# We can view all of the classes that automap found
Base.classes.keys()
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

# Create an app, being sure to pass __name__
app = Flask(__name__)

################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'start_date'<br/>"
        f"/api/v1.0/'start_date'/'end_date'<br/>"
    )
#####################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary of all precipitation data"""
    # Query all precipitation data
    date_prcp = session.query(Measurement.date, Measurement.prcp).\
        all()

    DP ={}
    for x in date_prcp:
        DP[x[0]] = x[1]

    session.close()

    return jsonify(DP)
################################

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    # Query all precipitation data
    stations_L1 = session.query(Measurement.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    stations_L2 = list(np.ravel(stations_L1))

    return jsonify(stations_L2)

#############################
@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of temps for last year"""
    #query
    last = session.query(Measurement.date).\
    order_by(Measurement.date).all()[-1:][0][0]
    minus_year = int(last[3])-1
    last_12 = f'{last[:3]}{minus_year}{last[4:]}'
    L_12 = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_12).all()
    
    session.close()

    # Convert list of tuples into normal list
    L__12 = list(np.ravel(L_12))

    return jsonify(L__12)

###############################
@app.route("/api/v1.0/<start>")
def start_only(start):
    """Returns data from a date onward"""
    range1 =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    range1_l = list(np.ravel(range1))

    return jsonify(range1_l)


#####################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Returns data from a date range"""
    range2 =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    range2_L = list(np.ravel(range2))

    return jsonify(range2_L)

##########################
if __name__ == "__main__":
    app.run(debug=True)