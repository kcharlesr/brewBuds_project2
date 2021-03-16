
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
#engine = create_engine(r'sqlite:///C:\Users\perki\Desktop\brewBuds_project2\brewBuds.sqlite', echo=False)
engine = create_engine('sqlite:///brewBuds.sqlite', echo=False)


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
Base = automap_base(metadata = metadata)
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
app = Flask(__name__)

#########################
#Flask Routes
#########################
#Home page
#List all routes available
@app.route("/")
def index():
    return render_template('index.html')
   
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
def bucks():
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
    
if __name__ == '__main__':
    app.run(debug = True)

