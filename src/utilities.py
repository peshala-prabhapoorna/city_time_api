from pydantic import BaseModel

class LocationEntry(BaseModel):
    country: str
    city: str
    name: str
    latitude: float
    longitude: float
    description: str
