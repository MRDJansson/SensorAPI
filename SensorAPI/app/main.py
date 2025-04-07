from fastapi import FastAPI
from .routes import sensors, blocks, readings, status
from contextlib import asynccontextmanager
from .database.database import create_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startataan")
    create_db()
    yield
    print("lopetellaan")


app = FastAPI(lifespan=lifespan)

app.include_router(sensors.router)
app.include_router(blocks.router)
app.include_router(readings.router)
app.include_router(status.router)