# city_time_api
current time of cities around the world
## running the API
1. create and activate a virtual environment
```bash
virtualenv venv
source venv/bin/activate # macOS and Linux
```
2. install dependencies
```bash
pip3 install -r requirements.txt
```
3. run the API (from project root)
```bash
fastapi dev src/main.py
```
## routes
1. GET - `/`  
this route returns a JSON object with `time_format`, `hours`, `minutes`,  
`seconds` keys. time format is 'utc' and other files contain current time in  
utc format.  
test:  
```bash
curl -X GET http://localhost:8000/
```
2. GET - `/tz/{city}`  
this route returns a JSON object with information related to time and  
location of the requested location in the {city} path parameter.
test:
```bash
curl -X GET http://localhost:8000/tz/Colombo
```
3. POST - `/city/`  
this route returns imformation about the nearest city in JSON format to the  
location specified with latitude and longtide inputs. 
test:
```bash
curl -X POST http://localhost:8000/city/ -H "Content-Type: application/json" -d '{"latitude": 6.927503832976636, "longitude": 79.85828762914382}'
```
3. GET - `/gap/`  
this route returns the time gap between two cities in the request in JSON  
format.  
test:
```bash
curl -X GET http://localhost:8000/gap/?Colombo&Tokyo
```
4. POST - `/add/`  
add locations to the database using this route.  
test:  
```bash
curl -X POST http://localhost:8000/add/ -H "Content-Type: application/json" -d '{"country": "Sri Lanka", "city": "Colombo", "name": "Lotus Tower", "latitude": 6.927503832976636, "longitude": 79.85828762914382, "description": "a big ol tower"}'
```
this program was developed using CPython 3.12.3.final.0
