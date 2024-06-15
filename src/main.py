from fastapi import FastAPI
from datetime import datetime
import sqlite3
import json

from locations_ball_tree import ball_tree, query_ball_tree, Location

app = FastAPI()

# connect to database and create a cursor
db_connection = sqlite3.connect("database/cities.db")
db_cursor = db_connection.cursor()

# create ball tree from city latitudes and longitidues
city_ball_tree = ball_tree(db_cursor)

@app.get("/")
async def root():
    utc_time = datetime.utcnow()

    return {"time_format": "utc",
            "hours": utc_time.hour,
            "minutes": utc_time.minute,
            "seconds": utc_time.second}

@app.get("/tz/{city}")
async def city_time(city: str):
    query = "SELECT country, city, timezone, utcoffset \
            FROM city_data \
            WHERE city=?;"
    query_result = db_cursor.execute(query, (city,))
    city_data = query_result.fetchone()

    return {"country": city_data[0],
            "city": city_data[1],
            "timezone": city_data[2],
            "utcoffset": city_data[3]}

@app.post("/city/")
async def nearest_city(location: Location):
    location = location.dict()
    distance, db_id = query_ball_tree(location, city_ball_tree)
    
    # query database to find the city
    query = "SELECT country, city, timezone, utcoffset \
            FROM city_data \
            WHERE id=?;"
    query_result = db_cursor.execute(query, (int(db_id),))
    city = query_result.fetchone()
    
    EARTH_RADIUS = 6371
    distance *= EARTH_RADIUS
    
    return {"country": city[0],
            "city": city[1],
            "timezone": city[2],
            "utcoffset": city[3],
            "distance": distance}

@app.get("/gap/")
async def time_difference(city_1: str, city_2: str):
    # query database to find cities
    query = "SELECT country, city, timezone, utcoffset \
           FROM city_data \
           WHERE city IN (?, ?);"
    query_result = db_cursor.execute(query, (city_1, city_2))
    cities = query_result.fetchall()

    # if either of the cities are not found return None
    if len(cities) !=2:
        return None
    
    # calculate time gap
    gap = 0
    if cities[0][1] == city_1:
        gap = cities[1][3] - cities[0][3]
    else:
        gap = cities[0][3] - cities[1][3]

    return {"city_1": city_1,
            "city_2": city_2,
            "gap": gap}
