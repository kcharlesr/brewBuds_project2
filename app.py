#design a Flask API based on the queries that you have just developed.
import datetime as dt
import numpy as np
import pandas as pd 

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, MetaData, Table, Column, Integer, String, Float, cast

from flask import Flask, jsonify

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

Table('top100', metadata,
     Column('Index', Integer, primary_key = True),
     Column('PostalCode',Integer),
     Column('Median_Income',Float),
     Column('Population',Float),
     Column('Median_age',Float), 
     Column('Keydemo_per',Float),
     Column('Brewery_count',Float),
     Column('Starbucks_count',Float),
     Column('pop_per_brewery',Float), 
     Column('pop_per_starbucks',Float),
     Column('Brewery_rank',Float), 
     Column('Income_rank',Float),
     Column('Demo_rank',Float),
     Column('Starbucks_rank',Float),
     Column('combined_score',Float), 
     Column('Total_rank',Float)    
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
top100= Base.classes.top100
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
        f"Top 100 Zip Codes:  /api/v1.0/top_zips<br/>"
        f"Breweries in Top 100 Zip Codes: /api/v1.0/breweries<br/>"
        f"Demographics in Top 100 Zip Codes:  /api/v1.0/demo<br/>"
        f"Existing Starbucks in Top 100 Zip Codes:  /api/v1.0/starbucks>"
        # f"Map: Existing Breweries for Recommended Places:  /api/v1.0/YYYY-MM-DD<start>/YYYY-MM-DD<end>"
        )

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
# @app.route("/api/v1.0/top_zips")
# def top_zip_list():
#     session = Session(engine)
#     top_zips = session.query(top100.PostalCode)
#     top_zip_list = []
#     for i in top_zips:
#         top_zip_list.append(i[0])
#     session.close()
#     return jsonify(top_zip_list)

@app.route("/api/v1.0/breweries")
def breweries():
    session = Session(engine)
    top_zips = session.query(top100.PostalCode)
    top_zip_list = []
    for i in top_zips:
        top_zip_list.append(i[0])
    brew_coord =session.query(brewery.PostalCode,brewery.Name, brewery.Latitude, brewery.Longitude).\
        order_by(top100.PostalCode.desc()).\
        filter(brewery.PostalCode.in_(top_zip_list)).\
        filter(brewery.PostalCode == top100.PostalCode).all()
    session.close()
    brew_geo = {
        "type": "FeatureCollection",
        "features": []
    }
    for i in brew_coord:
        feature = {"type": "Feature",
                "geometry":{
                    "type": "Point",
                    "coordinates":[i[3], i[2]]
                },
                "properties":{
                    "zipcode":i[0],
                    "name":i[1]
                }
                }
        brew_geo["features"].append(feature)
    return jsonify(brew_geo)

@app.route("/api/v1.0/demo")
def demographics():
    session = Session(engine)
    top_zips = session.query(top100.PostalCode)
    top_zip_list = []
    for i in top_zips:
        top_zip_list.append(i[0])
    top_full = session.query(brewery.PostalCode, top100.Brewery_count, brewery.Latitude, brewery.Longitude,top100.Median_Income,top100.Population,top100.pop_per_brewery,top100.pop_per_starbucks, top100.Keydemo_per).\
        order_by(top100.PostalCode.desc()).\
        group_by(top100.PostalCode).\
        filter(brewery.PostalCode.in_(top_zip_list)).\
        filter(brewery.PostalCode == top100.PostalCode).all()
    session.close()
    demo_geo = {
        "type": "FeatureCollection",
        "features": []
    }
    for i in top_full:
        feature = {"type": "Feature",
                "geometry":{
                    "type": "Point",
                    "coordinates":[i[3], i[2]]
                },
                "properties":{
                    "zipcode":i[0],
                    "brewery_count":i[1],
                    "median_income":i[4],
                    "population": i[5],
                    "pop_per_brewery": i[6],
                    "pop_per_starbucks": i[7],
                    "keydemo_per":i[8]
                    
                }
                }
        demo_geo["features"].append(feature)
    return jsonify(demo_geo)


@app.route("/api/v1.0/starbucks")
def starbucks():
    session =Session(engine)
    top_zips = session.query(top100.PostalCode)
    top_zip_list = []
    for i in top_zips:
        top_zip_list.append(i[0])
    starbucks_coord =session.query(starbucks.PostalCode, starbucks.Latitude, starbucks.Longitude).\
    order_by(starbucks.PostalCode).\
    filter(starbucks.PostalCode.in_(top_zip_list)).\
    filter(starbucks.PostalCode == top100.PostalCode).all()
    session.close()

    sbucks_geo = {
    "type": "FeatureCollection",
     "features": []
}
for i in starbucks_coord:
    feature = {"type": "Feature",
              "geometry":{
                  "type": "Point",
                  "coordinates":[i[2], i[1]]
              },
              "properties":{
                  "zipcode":i[0]
              }
              }
    sbucks_geo["features"].append(feature)
    return jsonify(sbucks_geo)
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


