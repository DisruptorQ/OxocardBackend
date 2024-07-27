from pydantic import BaseModel


class CreateSensorModel(BaseModel):
    name: str
