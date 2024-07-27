from datetime import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Response
from sqlalchemy.orm import Session

from oxocardendpoint.database import engine
from oxocardendpoint.entities.sensor import Sensor, SensorData
from oxocardendpoint.models.create_sensor_model import CreateSensorModel
from oxocardendpoint.models.sensor_data_model import LogSensorDataModel, SensorDataModel
from oxocardendpoint.models.sensor_model import SensorModel
from oxocardendpoint.services.sensor_data_service import SensorDataService
from oxocardendpoint.services.sensor_service import SensorService

router = APIRouter()


@router.get("/sensor/{name}")
async def get_sensor_by_name(name: str):
    with Session(engine) as session:
        service = SensorService(session)

        sensor = service.get_by_name(name=name)
        if sensor is None:
            return Response(content="Sensor not found!", status_code=404)


@router.post("/sensor/create")
async def create_sensor(model: CreateSensorModel):
    with Session(engine) as session:
        service = SensorService(session)
        sensor = service.get_by_name(name=model.name)
        if sensor is None:
            sensor = Sensor(name=model.name)
            session.add(sensor)
            session.commit()

        return SensorModel(id=sensor.id, name=sensor.name)


@router.get("/sensor/data/current")
async def get_current_sensor_data(sensor_name: Optional[str] = None):
    with Session(engine) as session:
        sensor_service = SensorService(session)
        sensor_data_service = SensorDataService(session)

        if sensor_name is None:
            data: List[Any] = sensor_data_service.get_current_data_all().all()

            current_data: List[SensorDataModel] = []
            for s_data in data:
                current_data.append(
                    SensorDataModel(
                        id=s_data.id,
                        sensorName=s_data.sensor_name,
                        timeStamp=s_data.time_stamp,
                        value=s_data.value,
                    )
                )
            return current_data

        print(f"SENSOR_NAME {sensor_name}")

        sensor = sensor_service.get_by_name(name=sensor_name)
        if sensor is None:
            return Response(content="Sensor not found!", status_code=404)

        sensor_data = sensor_data_service.get_current_data_single(sensor_id=sensor.id)
        if sensor_data is None:
            return Response(content="No sensor data available!", status_code=404)

        return SensorDataModel(
            id=sensor_data.id,
            sensorName=sensor.name,
            timeStamp=sensor_data.time_stamp,
            value=sensor_data.value,
        )


@router.post("/sensor/data")
async def log_sensor_data(model: LogSensorDataModel):
    with Session(engine) as session:
        service = SensorService(session)
        sensor = service.get_by_name(name=model.sensorName)
        if sensor is None:
            return Response(content="Sensor not found!", status_code=404)

        sensor_data = SensorData(
            sensor=sensor, time_stamp=datetime.now(), value=model.value
        )

        session.add(sensor_data)
        session.commit()
        session.close()

    return Response(content="Data logged.", status_code=200)
