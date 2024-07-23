from fastapi import FastAPI

from oxocardendpoint.database import create_schema, new_session
from oxocardendpoint.entities.sensor import Sensor
from oxocardendpoint.services.sensor_service import SensorService

create_schema()

new_sensor = Sensor()
new_sensor.name = "Test"

session = new_session()

session.add(new_sensor)
session.commit()


app = FastAPI()


@app.get("/")
async def hello_world():
    return "{'Test': 'Hello'}"


@app.get("/sensor/data")
async def receive_sensor_data():
    service = SensorService()

    sensor = service.get_by_name()
    return {"status": sensor.name}
