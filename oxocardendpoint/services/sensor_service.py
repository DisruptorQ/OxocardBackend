from sqlalchemy.orm import Session

from oxocardendpoint.database import new_session
from oxocardendpoint.entities.sensor import Sensor


class SensorService:
    def get_session(self) -> Session:
        return new_session()

    def get_by_name(self) -> Sensor | None:
        session = self.get_session()
        return session.query(Sensor).filter(Sensor.name == "Test").first()
