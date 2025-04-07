from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from ..database import crud, database, models

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_sensor(sensor: models.SensorIn, session: Session = Depends(database.get_session)):
    return crud.create_sensor(session, sensor)

@router.put("/{sensor_id}/status", response_model=models.SensorDb)
def update_sensor_status(sensor_id: int, is_error: bool, session: Session = Depends(database.get_session)):
    return crud.update_sensor_status(session, sensor_id, is_error)

@router.put("/{sensor_id}/block", response_model=models.SensorDb)
def update_sensor_block(sensor_id: int, block_id: int, session: Session = Depends(database.get_session)):
    return crud.update_sensor_block(session, sensor_id, block_id)

@router.delete("/{reading_id}")
def delete_reading(reading_id: int, session: Session = Depends(database.get_session)):
    return crud.delete_reading(session, reading_id)

@router.get("/", response_model=list[models.SensorDb])
def get_sensors(block_id: int = None, session: Session = Depends(database.get_session)):
    return crud.get_sensors(session, block_id)

@router.get("/{sensor_id}", response_model=models.SensorDb)
def get_sensor(sensor_id: int, session: Session = Depends(database.get_session)):
    return crud.get_sensor(session, sensor_id)

@router.get("/{sensor_id}/sensor_status", response_model=list[models.SensorStatusDb])
def get_sensor_status(sensor_id: int, session: Session = Depends(database.get_session)):
    return crud.get_sensor_status(session, sensor_id)

@router.get("/", response_model=list[models.SensorDb])
def get_sensors_by_status(is_error: bool = None, session: Session = Depends(database.get_session)):
    return crud.get_sensors_by_status(session, is_error)