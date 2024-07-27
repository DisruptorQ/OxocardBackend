from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LogSensorDataModel(BaseModel):
    sensorName: str
    value: str


class SensorDataModel(LogSensorDataModel):
    id: Optional[int]
    timeStamp: Optional[datetime]
