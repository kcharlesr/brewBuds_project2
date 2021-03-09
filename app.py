#design a Flask API based on the queries that you have just developed.
import datetime as dt
import numpy as np
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#########################
# Database Setup
#########################
#ENGINE #1
engine1 = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)

# reflect an existing database into a new model
Base1 = automap_base()

#reflect the tables
Base1.prepare(engine1, reflect=True)

#save reference to  the tables
Starbucks = Base1.classes.starbucks


# #ENGINE 2
# engine2 = create_engine("sqlite:///./Resources/hawaii.sqlite", echo=False)

# # reflect an existing database into a new model
# Base2 = automap_base()

# #reflect the tables
# Base2.prepare(engine2, reflect=True)

# #save reference to  the tables
# Measurement = Base.classes.measurement
# Station = Base.classes.station
##########################
#Flask Setup
##########################
#initialize Flask app
app=Flask(__name__)

#########################
#Flask Routes
#########################
#Home page
#List all routes available
@app.route("/")
def index():
    return(
        f"Home Base!<br/>"
        f"Available routes:<br/>"
        f"Defining the Starbucks Standard:  /api/v1.0/precipitation<br/>"
        f"Defining the Brewery Standard: /api/v1.0/stations<br/>"
        f"Map: Recommended places' population:  /api/v1.0/tobs<br/>"
        f"Map: Recommended places' median income  /api/v1.0/YYYY-MM-DD<start><br/>"
        f"Map: Existing Starbucks for Recommended Places:  /api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end>"
        f"Map: Existing Breweries for Recommended Places:  /api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end>"
        )

# @app.route("/api/v1.0/brewery_standard")
# def precip():
#     session = Session(engine)
#     year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
#     results = session.query(Measurement.date, Measurement.prcp)\
#         .filter(Measurement.date >= year_ago).all()
#     session.close()
 
#     #Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#     all_results = []
   
#     for date, prcp in results:
#         prcp_dict = {}
#         prcp_dict["date"] = date
#         #prcp_dict[0] = int(date)
#         prcp_dict["prcp"] = prcp
#         all_results.append(prcp_dict)
    

#     #Return the JSON representation of your dictionary.
#     return jsonify(all_results)

# @app.route("/api/v1.0/Starbucks_standard")
# def stations():
#     #Return a JSON list of stations from the dataset.
#     session = Session(engine)
#     results = session.query(Measurement.station).distinct().all()
#     session.close()

#     active_stations = list(np.ravel(results))
    
#     return jsonify(active_stations)
@app.route("/api/v1.0/Existing_Starbucks")
def stations():
    #Return a JSON list of Starbucks from the dataset.
    session = Session(engine)
    results = session.query(Measurement.station).distinct().all()
    session.close()

    active_stations = list(np.ravel(results))
    
    return jsonify(active_stations)


# @app.route("/api/v1.0/tobs")
# def tobs():
#     # Query the dates and temperature observations of the most active station for the last year of data.
#    session=Session(engine)
#    year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
#    most_active_station = session.query(Measurement.station, func.count(Measurement.station))\
#         .filter(Measurement.date >= year_ago)\
#         .group_by(Measurement.station)\
#         .order_by(func.count(Measurement.station).desc()).first()
#    temps = session.query(Measurement.tobs)\
#         .filter(Measurement.station == most_active_station[0])\
#         .filter(Measurement.date >= year_ago).all()
#    session.close()
#    # Return a JSON list of temperature observations (TOBS) for the previous year.
#    return_temps = [result[0] for result in temps]
#    return jsonify(return_temps)

#  # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

#   # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

#   # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# @app.route("/api/v1.0/<start>")
# def start(start):
#     if len(start) == 10: 
#         session=Session(engine)
#         results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
#             .filter(Measurement.date >= start).all()
#         session.close()
#         return jsonify(results)
    
#     return jsonify({"error": f"{start} is not in valid date format.  Please try again with format YYYY-MM-DD."}),404

# @app.route("/api/v1.0/<start>/<end>")
# def start_end(start, end):
#     if len(start) == 10 and len(end) == 10: 
#         session=Session(engine)
#         results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
#             .filter(Measurement.date >= start)\
#             .filter(Measurement.date <= end).all()
#         session.close()
#         return jsonify(results)
    
#     return jsonify({"error": f"{start} or {end} is not in valid date format.  Please try again with format YYYY-MM-DD."}),404
    
 

if __name__ == '__main__':
    app.run(debug = True)


