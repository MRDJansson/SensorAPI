from sqlmodel import SQLModel, Field
from datetime import datetime

# En tiedä vielä yhtään tuleeko tämäntyyppinen ratkaisu toimimaan viiteavainten suhteen, mutta korjataan projektin edetessä!

# Perusluokka lohkoille, sisältää nimen
class BlockBase(SQLModel):
    name: str

# Lohkojen db, perii perusluokan ja sisältää id:n
class BlockDb(BlockBase, table=True):
    id: int = Field(default=None, primary_key=True)

# Syöttömalli lohkoille, perii perusluokan
class BlockIn(BlockBase):
    pass

# Perusluokka antureille, sisältää tunnisteen, id:n, tilan ja virhetilan
class SensorBase(SQLModel):
    sensor_id: int
    block_id: int
    is_active: bool
    is_error: bool

# Antureiden db, perii Baseluokan ja sisältää id:n
class SensorDb(SensorBase, table=True):
    id: int = Field(default=None, primary_key=True)

# Syöttömalli antureille, perii myös baseluokan
class SensorIn(SensorBase):
    pass

# Perusluokka lämpötilanmittauksille, sisältää anturin id:n, lämpötilan ja timestämpin
class TemperatureReadingBase(SQLModel):
    sensor_id: int
    temperature: float
    time: datetime

# Lämpötilamittausten db, perii perusluokan ja sisältää id:n
class TemperatureReadingDb(TemperatureReadingBase, table=True):
    id: int = Field(default=None, primary_key=True)

# Syöttömalli lämpötilamittauksille, perii perusluokan
class TemperatureReadingIn(TemperatureReadingBase):
    pass

# Perusluokka tilamuutoksille, sisältää anturin id:n, virhetilan ja timestämpin
class SensorStatusBase(SQLModel):
    sensor_id: int
    is_error: bool
    time: datetime

# Tilamuutosten taulu, peruu baseluokan ja sisältää id:n
class SensorStatusDb(SensorStatusBase, table=True):
    id: int = Field(default=None, primary_key=True)

# Syötemalli tilamuutoksille, perii baseluokan
class SensorStatusIn(SensorStatusBase):
    pass