from pydantic import BaseModel


class SensorModel(BaseModel):
    id: int
    name: str
