from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from oxocardendpoint.controllers import sensor_controller
from oxocardendpoint.database import create_schema

create_schema()

origins = ["http://localhost:4200"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sensor_controller.router)
