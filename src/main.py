from fastapi import FastAPI
from datetime import datetime
from sklearn.neighbors import BallTree
import sqlite3
import numpy as np

app = FastAPI()

# connect to database and create a cursor
db_connection = sqlite3.connect("database/cities.db")
db_cursor = db_connection.cursor()

@app.get("/")
async def root():
    utc_time = datetime.utcnow()
    return {"time_format": "utc",
            "hours": utc_time.hour,
            "minutes": utc_time.minute,
            "seconds": utc_time.second}

@app.get("/tz/{city}")
async def city_time(city):
    query = f"SELECT country, city, timezone, utcoffset \
                FROM city_data \
                WHERE city='{city}';"
    query_result = db_cursor.execute(query)
    city_data = query_result.fetchone()

    return {"country": city_data[0],
            "city": city_data[1],
            "timezone": city_data[2],
            "utcoffset": city_data[3]}
