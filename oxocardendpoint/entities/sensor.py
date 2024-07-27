from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from oxocardendpoint.entities.base import Base


class Sensor(Base):
    __tablename__ = "sensor"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    sensor_datas: Mapped[List["SensorData"]] = relationship(back_populates="sensor")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sensor_id: Mapped[int] = mapped_column(Integer, ForeignKey("sensor.id"))
    time_stamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)

    sensor: Mapped["Sensor"] = relationship(back_populates="sensor_datas")
