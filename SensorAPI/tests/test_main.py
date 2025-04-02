from fastapi import FastAPI

app = FastAPI()

sensors = [
    {"id": 0, "sensor_id": 11, "block": "A13_13", "is_active": True,  "is_error": False},
    {"id": 1, "sensor_id": 1,  "block": "A14_0",  "is_active": True,  "is_error": True},
    {"id": 2, "sensor_id": 17, "block": "B1_2",   "is_active": False, "is_error": False},
]


@app.get("/sensors")
def get_sensors(block: str = ""):
    if block:
        return [s for s in sensors if s["block"] == block]
    return sensors


@app.get("/sensors/{sensor_id}")
def get_sensor_by_id(sensor_id: int):
    return sensors[sensor_id]
