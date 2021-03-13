
#design a Flask API based on the queries that you have just developed.
import datetime as dt
import numpy as np
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, MetaData, Table, Column, Integer, String, Float, cast

from flask import Flask, jsonify, render_template

#########################
# Database Setup
#########################
#ENGINE
engine = create_engine("sqlite:///brewBuds.sqlite", echo=False)

#BUILD THE TABLES
metadata = MetaData()
Table('brewery', metadata,
     Column('Index', Integer, primary_key = True),
     Column('City', String),
     Column('Latitude',Float),
     Column('Longitude',Float),
     Column('Name',String),
     Column('PostalCode',Integer),
     Column('State', String))

Table('starbucks', metadata,
     Column('Index', Integer, primary_key = True),
     Column('State', String),
     Column('PostalCode',Integer),
     Column('Longitude',Float),
     Column('Latitude',Float)
     )

Table('income', metadata,
     Column('Index', Integer, primary_key = True),
     Column('PostalCode',Integer),
     Column('Median_Income',Float),
     Column('Population',Float),
     Column('Median_age',Float), 
     Column('Keydemo_per',Float)
     )

# reflect an existing database into a new model
Base = automap_base(metadata=metadata)
# reflect the tables
#Base.prepare()

#reflect the tables
Base.prepare(engine, reflect=True)

#save reference to  the tables
starbucks = Base.classes.starbucks
income = Base.classes.income
brewery = Base.classes.brewery

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
    return render_template('index.html')
    # ( 
    #     f"Home Base!<br/>"
    #     f"Available routes:<br/>"
    #     f"Breweries per Zip Code:  /api/v1.0/brew_zip<br/>"
    #     f"Defining the Brewery Standard: /api/v1.0/stations<br/>"
    #     f"Map: Recommended places' population:  /api/v1.0/tobs<br/>"
    #     f"Map: Recommended places' median income  /api/v1.0/YYYY-MM-DD<start><br/>"
    #     f"Map: Existing Starbucks for Recommended Places:  /api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end>"
    #     f"Map: Existing Breweries for Recommended Places:  /api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end>"
    #     )
@app.route("/map")
def leaflet():
    return render_template('leaflet.html')

@app.route("/scatter")
def scatter():
    return render_template('scatter.html')


@app.route("/data")
def data():
    return render_template('data.html')

@app.route("/api/v1.0/brew_zip")
def brew_zip():
    session = Session(engine)
    brew_count_zip = session.query(brewery.PostalCode, func.count(brewery.Name)).\
        group_by(brewery.PostalCode).\
        order_by(func.count(brewery.Name).desc()).all()
    session.close()
 
    #Convert the query results to a dictionary using `PostalCode` as the key and `count` as the value.
    all_results = []
   
    for pc, count in brew_count_zip:
        pc_dict = {}
        pc_dict["zip_code"] = pc
        #prcp_dict[0] = int(date)
        pc_dict["count"] = count
        all_results.append(pc_dict)
 
     #Return the JSON representation of your dictionary.
    return jsonify(all_results)

# @app.route("/api/v1.0/Starbucks_standard")
# def stations():
#     #Return a JSON list of stations from the dataset.
#     session = Session(engine)
#     results = session.query(Measurement.station).distinct().all()
#     session.close()

#     active_stations = list(np.ravel(results))
    
#     return jsonify(active_stations)
# @app.route("/api/v1.0/Existing_Starbucks")
# def stations():
#     #Return a JSON list of Starbucks from the dataset.
#     session = Session(engine)
#     results = session.query(Measurement.station).distinct().all()
#     session.close()

#     active_stations = list(np.ravel(results))
    
#     return jsonify(active_stations)


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
