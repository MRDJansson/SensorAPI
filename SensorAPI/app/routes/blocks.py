from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..database import crud, database, models

router = APIRouter()

@router.get("/{block_id}/sensors", response_model=list[models.SensorDb])
def get_sensors_by_block(block_id: int, session: Session = Depends(database.get_session)):
    return crud.get_sensors_by_block(session, block_id)