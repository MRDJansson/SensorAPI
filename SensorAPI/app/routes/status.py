from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database import crud, database, models

router = APIRouter()

@router.get("/{sensor_id}", response_model=list[models.SensorStatusDb])
def get_sensor_status(sensor_id: int, session: Session = Depends(database.get_session)):
    return crud.get_sensor_status(session, sensor_id)

@router.get("/error-graph")
def get_error_graph(session: Session = Depends(database.get_session)):
    return crud.get_error_graph(session)