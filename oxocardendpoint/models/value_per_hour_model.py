from datetime import datetime

from pydantic import BaseModel


class ValuePerHour(BaseModel):
    time_stamp: datetime
    value: float
