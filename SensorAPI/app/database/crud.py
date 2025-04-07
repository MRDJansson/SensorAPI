from sqlmodel import Session, select
from datetime import datetime
from fastapi import HTTPException
from ..database.models import SensorDb, SensorIn, TemperatureReadingDb, SensorStatusDb, BlockDb

# Palastellaan myöhemmin pieniin crudeihin


## Hallinnolliset toiminnot

def create_sensor(session: Session, sensor_in: SensorIn):
    db_sensor = SensorDb.model_validate(sensor_in)
    session.add(db_sensor)
    session.commit()
    session.refresh(db_sensor)
    return db_sensor

def update_sensor_status(session: Session, sensor_id: int, is_error: bool):
    sensor = session.get(SensorDb, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    sensor.is_error = is_error
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

def update_sensor_block(session: Session, sensor_id: int, block_id: int):
    sensor = session.get(SensorDb, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    sensor.block_id = block_id
    session.add(sensor)
    session.commit()
    session.refresh(sensor)
    return sensor

def delete_reading(session: Session, reading_id: int):
    reading = session.get(TemperatureReadingDb, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    session.delete(reading)
    session.commit()
    return reading


## Mittaukset ja hallinta

def get_sensors(session: Session, block_id: int = None):
    statement = select(SensorDb)
    if block_id is not None:
        statement = statement.where(SensorDb.block_id == block_id)
    sensors = session.exec(statement).all()
    if not sensors:
        raise HTTPException(status_code=404, detail="No sensors found")
    return sensors

def get_sensor(session: Session, sensor_id: int):
    sensor = session.get(SensorDb, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor

def get_sensors_by_block(session: Session, block_id: int):
    sensors = session.exec(select(SensorDb).where(SensorDb.block_id == block_id)).all()
    if not sensors:
        raise HTTPException(status_code=404, detail="No sensors found in this block")
    return sensors

def get_readings(session: Session, sensor_id: int, limit: int = 10, start: datetime = None, end: datetime = None):
    statement = select(TemperatureReadingDb).where(TemperatureReadingDb.sensor_id == sensor_id)
    if start and end:
        statement = statement.where(TemperatureReadingDb.time.between(start, end))
    statement = statement.order_by(TemperatureReadingDb.time.desc()).limit(limit)
    readings = session.exec(statement).all()
    if not readings:
        raise HTTPException(status_code=404, detail="No readings found")
    return readings

def get_sensors_by_status(session: Session, is_error: bool = None):
    statement = select(SensorDb)
    if is_error is not None:
        statement = statement.where(SensorDb.is_error == is_error)
    sensors = session.exec(statement).all()
    if not sensors:
        raise HTTPException(status_code=404, detail="No sensors found with this status")
    return sensors

def get_error_graph(session: Session):
    # placeholder, kunnes keksin miten tämä ratkaistaan
    return {"error_graph": []}