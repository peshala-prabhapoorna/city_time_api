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
