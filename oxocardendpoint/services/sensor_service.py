from typing import List

from sqlalchemy.orm import Session

from oxocardendpoint.entities.sensor import Sensor
from oxocardendpoint.services.base_service import BaseService


class SensorService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_by_name(self, name: str) -> Sensor | None:
        return self.session.query(Sensor).filter(Sensor.name == name).first()

    def get_all(self) -> List[Sensor]:
        return self.session.query(Sensor).all()
