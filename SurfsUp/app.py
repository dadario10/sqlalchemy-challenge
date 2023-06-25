# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables.
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)  

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    ## set up welcome page, and links to routes for data
    return (
        f"<h1>SQLAlchemy Challenge</h1>"
        f"<h1>Part 2: Climate App</h1>"
        f"<h2>Here are the available climate routes:</h2>"

        f"<ol>Precipitation analysis - The last 12 months of data:<br/>" 
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/precipitation>"
        f"/api/v1.0/precipitation</a></li><br/><br/>"

        f"Stations Analysis - List of stations:<br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/stations>"
        f"/api/v1.0/stations</a></li><br/><br/>"
        
        f"Temperature Analysis - List of temperature observations of the most-active station for the previous year of data:<br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/tobs>"
        f"/api/v1.0/tobs</a></li><br/><br/>"

        f"List of the minimum, average, and maximum temperature for a specified start date:<br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/2017-08-23>"
        f"/api/v1.0/start</a></li><br/><br/>"

        f"List of the Minimum, Average, and Maximum temperature for a specified start and end date: <br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/2016-08-23/2017-08-23>"
        f"/api/v1.0/start/end</a></li></ol><br/>"
        f"By Dario Micucci<br/>"

    )

# Precipitation Analysis:

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Date for one year from the last data point 
    last_years_data = session.query(
        measurement.date).order_by(measurement.date.desc()).first()
    (recent_date, ) = last_years_data
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    recent_date = recent_date.date()
    last_years_date = recent_date - relativedelta(years=1)

    # Retrieve precipitation data 
    last_data = session.query(measurement.date, measurement.prcp).filter(
        measurement.date >= last_years_date).all()

    session.close()

    # Convert results to a dictionary 
    prec_dictionary = []
    for date, prcp in last_data:
        if prcp != None:
            prcp_dict = {}
            prcp_dict[date] = prcp
            prec_dictionary.append(prcp_dict)

    # Return the JSON representation of the dictionary
    return jsonify(prec_dictionary)

# Stations Analysis:

@app.route("/api/v1.0/stations")
def stations():
   results = session.query(station.station).all()
   session.close()
    # Unravel results into a 1D array and convert to a list
   stations = list(np.ravel(results))
   return jsonify(stations=stations)

# Temperature Analysis:

@app.route("/api/v1.0/tobs")
def tobs():

    # Date for one year ago from the last data point in the database
    last_years_data = session.query(
        measurement.date).order_by(measurement.date.desc()).first()
    (recent_date, ) = last_years_data
    recent_date = dt.datetime.strptime(recent_date, '%Y-%m-%d')
    recent_date = recent_date.date()
    last_years_date = recent_date - relativedelta(years=1)

    # The most active station
    most_active_station = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count().desc()).\
        first()

    # Station ID number
    (active_station_id, ) = most_active_station
    print(
        f"The most active station is {active_station_id}.")

    # Query the dates and temperature observations of the most-active station for the previous year of data
    last_years_data = session.query(measurement.date, measurement.tobs).filter(
        measurement.station == active_station_id).filter(measurement.date >= last_years_date).all()

    session.close()

    # Convert results to a dictionary
    all_temps_dict = []
    for date, temp in last_years_data:
        if temp != None:
            temps_dict = {}
            temps_dict[date] = temp
            all_temps_dict.append(temps_dict)

    # Return the JSON representation of the dictionary
    return jsonify(all_temps_dict)

# Minimum, Maximum and Average temperature for specific start/end dates:

@app.route('/api/v1.0/<start>', defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def temps_for_date_range(start, end):

    # If there is a start date and an end date
    if end != None:
        temps_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).filter(
            measurement.date <= end).all()
    # If we only have a start date
    else:
        temps_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

    session.close()

    # Convert the results to a list
    temps_list = []
    no_temps_data = False
    for min_temp, avg_temp, max_temp in temps_data:
        if min_temp == None or avg_temp == None or max_temp == None:
            no_temps_data = True
        temps_list.append(min_temp)
        temps_list.append(avg_temp)
        temps_list.append(max_temp)

    # Return the JSON representation of dictionary
    if no_temps_data == True:
        return f"There is no temperature data found for the chosen date range"
    else:
        return jsonify(temps_list)


if __name__ == '__main__':
    app.run(debug=True)

