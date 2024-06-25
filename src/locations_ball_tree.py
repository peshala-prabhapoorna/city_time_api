from sklearn.neighbors import BallTree
from pydantic import BaseModel
import numpy as np


class Location(BaseModel):
    latitude: float
    longitude: float


def ball_tree(db_cursor):
    # get latitudes, longitude from database
    query = "SELECT latitude, longitude FROM city_data;"
    query_result = db_cursor.execute(query)
    locations = query_result.fetchall()

    # convert degress to radian and locations to 2d list
    locations = [
        [np.deg2rad(latitude), np.deg2rad(longitude)]
        for (latitude, longitude) in locations
    ]
    # convert locations to a numpy array
    locations = np.array(locations)

    # create ball tree of locations
    bt = BallTree(locations, metric="haversine")

    return bt


def query_ball_tree(location, ball_tree):
    query_location = [location["latitude"], location["longitude"]]
    # convert degrees to radians
    query_location = np.deg2rad(query_location)
    query_location = np.array([query_location])

    distances, indices = ball_tree.query(query_location, k=1)

    return distances[0][0], indices[0][0] + 1
