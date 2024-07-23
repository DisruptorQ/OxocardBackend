from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from oxocardendpoint.entities.base import Base

engine = create_engine("sqlite:///foo.db", echo=True)
new_session = sessionmaker(bind=engine)


def create_schema():
    Base.metadata.create_all(engine)
