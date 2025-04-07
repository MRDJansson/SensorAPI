from fastapi import APIRouter, Depends
from sqlmodel import Session
from datetime import datetime
from ..database import crud, database, models

router = APIRouter()

@router.get("/{sensor_id}", response_model=list[models.TemperatureReadingDb])
def get_readings(sensor_id: int, limit: int = 10, start: datetime = None, end: datetime = None, session: Session = Depends(database.get_session)):
    return crud.get_readings(session, sensor_id, limit, start, end)

@router.delete("/{reading_id}")
def delete_reading(reading_id: int, session: Session = Depends(database.get_session)):
    return crud.delete_reading(session, reading_id)