# SensorAPI

# Teollisuushallin lämpötila-antureiden REST API - Suunnitelma

## Alustava aikataulu (ei tule pitämään 😅)
- **Päivä 1-2**: Suunnittelu
- **Päivä 3-4**: Projektin alustus ja tietokantamalli
- **Päivä 5**: Erikoishaut ja virheenkäsittely
- **Päivä 6**: Testaus ja dokumentointi
- **Päivä 7**: Viimeistely ja raportin kirjoitus

## Tavoite
Toteuttaa REST API, joka hallinnoi tehdashallin lämpötila-antureita. API tarjoaa endpointit anturien hallintaan, lämpötilamittausten keräämiseen sekä datan hakemiseen.

## Käytetyt teknologiat
Projektissa käytetään samoja teknologioita kuin kurssin aikana:

- **FastAPI**: Python-web-framework REST API:n toteutukseen
- **SQLite**: Kevyt tietokantaratkaisu
- **SQLAlchemy**: ORM, joka mahdollistaa tietokannan käytön ilman suoria SQL-kyselyitä
- **Pydantic**: Datan validointiin ja mallintamiseen

### Perustelut:
- **FastAPI**: Nopeus, helppokäyttöisyys ja automaattinen dokumentaatio.
- **SQLite**: Kevyt ja erillistä tietokantapalvelinta ei tarvita.
- **SQLAlchemy**: Ylläpidettävyyden ja kehityksen helpottamiseksi.
- **Pydantic**: Varmistaa datan oikeellisuuden API:ssa.

---

## Tietokantarakenne

### **Lohkot (blocks)**
| Nimi | Tyyppi | Kuvaus |
|------|--------|---------|
| `id` | int | Uniikki tunniste |
| `name` | str | Lohkon nimi (esim. A_13_13) |

### **Anturit (sensors)**
| Nimi | Tyyppi | Kuvaus |
|------|--------|---------|
| `id` | int | Uniikki tunniste |
| `sensor_id` | int | Anturin tunniste (esim. 11, 32) |
| `block_id` | int | Viite `blocks.id`:hen |
| `is_active` | bool | Onko käytössä |
| `is_error` | bool | Onko virhetilassa |

### **Lämpömittaukset (temperature_readings)**
| Nimi | Tyyppi | Kuvaus |
|------|--------|---------|
| `id` | int | Uniikki tunniste |
| `sensor_id` | int | Viite `sensors.id`:hen |
| `temperature` | float | Lämpötila (C, 1 desimaali) |
| `time` | DateTime | Mittauksen ajankohta |

### **Tilamuutokset (sensor_status)**
| Nimi | Tyyppi | Kuvaus |
|------|--------|---------|
| `id` | int | Uniikki tunniste |
| `sensor_id` | int | Viite `sensors.id`:hen |
| `is_error` | bool | Virhetila: True |
| `time` | DateTime | Muutoksen ajankohta |

### Perustelut:
Tehtävänantona oli, että on lohkoja joiden sisällä on antureita ja antureilla on tiettyjä toimintoja. Tällöin oli loogista:
- **Lohkot (`blocks`) ja anturit (`sensors`) erillisinä**: Yksi lohko voi sisältää useita antureita.
- **Lämpötilamittaukset (`temperature_readings`) erillisenä tauluna**: Mittaushistorian säilyttämistä varten.
- **Tilamuutokset (`sensor_status`) erillisenä tauluna**: Anturin tilahistorian seuraamiseen.

---

## Toiminnallisuudet

### **Hallinnan toiminnot**
| Toiminto | Metodi | Endpoint |
|----------|--------|----------|
| Lisää uusi anturi | `POST` | `/sensors/` |
| Muuta anturin tilaa | `PUT` | `/sensors/{sensor_id}/status` |
| Muuta lohkoa | `PUT` | `/sensors/{sensor_id}/block` |
| Poista mittaustulos | `DELETE` | `/sensors/{reading_id}` |

### **Mittaukset ja hallinta**
| Toiminto | Metodi | Endpoint |
|----------|--------|----------|
| Listaa kaikki anturit | `GET` | `/sensors/` |
| Listaa tietyn lohkon anturit | `GET` | `/blocks/{block_id}/sensors` |
| Näytä anturin kaikki tiedot | `GET` | `/sensors/{sensor_id}` |
| 10 uusinta mittaustulosta | `GET` | `/sensors/{sensor_id}/readings?limit=10` |
| Mittausten aikaväli | `GET` | `/sensors/{sensor_id}/readings?start=yyyy-mm-dd&end=yyyy-mm-dd` |
| Anturin tilahistoria | `GET` | `/sensors/{sensor_id}/sensor_status` |
| Hae anturit tilan mukaan | `GET` | `/sensors?is_error=true` |
| Virhetila-graafi (?) | `GET` | `/sensor_status/error-graph` (tarkennetaan myöhemmin) |

---

## Asennus ja alustus

## Alustus ja asennukset

1. **Virtuaaliympäristön luominen:**
   
   Luo virtuaaliympäristö seuraavalla komennolla:
   `python -m venv venv`

2. **FastAPI:n asennus:**
   
   Asenna FastAPI: 
   `pip install "fastapi[standard]"`
   
   Päivitä pip:
   `python.exe -m pip install --upgrade pip`

3. **SQLite:n asennus:**
   
   Asenna SQLite:
   `pip install sqlite`

4. **SQLAlchemy:n asennus:**
   
   Asenna SQLAlchemy:
   `pip install sqlalchemy`