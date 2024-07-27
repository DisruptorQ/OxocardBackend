from sqlalchemy import MetaData, create_engine

from oxocardendpoint.entities.base import Base

engine = create_engine("sqlite:///sqlite.db", echo=True)
metadata: MetaData = Base.metadata


def create_schema():
    Base.metadata.create_all(engine)
