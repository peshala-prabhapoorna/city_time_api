from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    utc_time = datetime.utcnow()
    return {"time_format": "utc", "hours": utc_time.hour, "minutes": utc_time.minute, "seconds": utc_time.second}
