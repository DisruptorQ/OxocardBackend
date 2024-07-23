from sqlalchemy.orm import Mapped, mapped_column

from oxocardendpoint.entities.base import Base


class Sensor(Base):
    __tablename__ = "sensor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
