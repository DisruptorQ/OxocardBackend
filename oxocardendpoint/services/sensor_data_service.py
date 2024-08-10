from datetime import datetime
from typing import List

from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from oxocardendpoint.database import metadata
from oxocardendpoint.entities.sensor import Sensor, SensorData
from oxocardendpoint.services.base_service import BaseService


class SensorDataService(BaseService):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

    def get_current_data_single(self, sensor_id: int) -> SensorData | None:
        return (
            self.session.query(SensorData)
            .filter(SensorData.sensor_id == sensor_id)
            .order_by(desc(SensorData.time_stamp))
            .first()
        )

    def get_all_data_for_day(self, date: datetime) -> List[SensorData]:
        return (
            self.session.query(SensorData)
            .filter(func.date(SensorData.time_stamp) == date.date())
            .order_by(asc(SensorData.time_stamp))
            .all()
        )

    def get_current_data_all(self):
        sensor = metadata.tables[Sensor.__tablename__]
        sensor_data = metadata.tables[SensorData.__tablename__]

        joined_tables = sensor_data.join(sensor, sensor_data.c.sensor_id == sensor.c.id)

        subquery = (
            select(
                sensor_data.c.id,
                sensor.c.name.label("sensor_name"),
                sensor_data.c.sensor_id,
                sensor_data.c.time_stamp,
                sensor_data.c.value,
                func.row_number()
                .over(
                    partition_by=sensor_data.c.sensor_id,
                    order_by=desc(sensor_data.c.time_stamp),
                )
                .label("rn"),
            )
            .select_from(joined_tables)
            .subquery()
        )

        query = select(
            subquery.c.id,
            subquery.c.sensor_name,
            subquery.c.sensor_id,
            subquery.c.time_stamp,
            subquery.c.value,
        ).where(subquery.c.rn == 1)

        return self.session.execute(query)
