# AnturiAPI

## Teollisuushallin lämpötila-antureiden REST API - Suunnitelma

## Alustava aikataulu (ei tule pitämään 😅)
- **Kerta 1-2**: Suunnittelu
- **Kerta 3-4**: Projektin alustus ja tietokantamalli
- **Kerta 5**: Erikoishaut ja virheenkäsittely
- **Kerta 6**: Testaus ja dokumentointi
- **Kerta 7**: Viimeistely ja raportin kirjoitus

## Tavoite
Toteuttaa REST API (AnturiAPI), joka hallinnoi tehdashallin lämpötila-antureita. API tarjoaa endpointit anturien hallintaan, lämpötilamittausten keräämiseen sekä datan hakemiseen.

## Alustus
Tehdashalleja (lohkoja) on 3 kappaletta. Jokaisessa lohkossa on 2-3 nimettyä uniikkia lämpötila-anturia.
Anturit ovat Raspberry PI-rakennelmia, jotka lähettävät tietyin väliajoin datapaketin palvelimelle. Tällä hetkellä anturit mittaavat vain lämpötilaa, mutta laajennukset ovat mahdollisia.
Jokainen anturi tietää oman uniikin tunnisteensa, mutta se ei tiedä mihin lohkoon se kuuluu.
Lohkot ovat käyttäjien määrittelemiä fyysisiä alueita ja jokainen anturi kuuluu johonkin lohkoon. Lohkossa on vähintään yksi anturi.
Anturit mittaavat ja lähettävät lämpötila-arvon yhden desimaalin tarkkuudella Celsius-asteisena.
Koska anturit ovat kustomoituja ja tähän kohteeseen tehtyjä, niissä on sisäänrakennettuna pientä automatiikkaa. 
Anturi tunnistaa milloin se on virhetilassa (ei-normaalissa toimintatilassa).
Joutuessaan virhetilaan anturi lähettää tästä tiedon palvelimelle, jolloin ihminen pääsee tarkastamaan tilanteen. 
Virhetilassa ollessaan anturi ei lähetä lämpötilatietoja ja sen tila voidaan muuttaa takaisin normaaliin toimintatilaan vain ohjelmallisesti ulkopuolisen toimijan toimesta. 
Nykyinen versio anturista ei vielä tiedä mikä virhe siinä on, joten se osaa kertoa vain yleisestä virheestä.

---

## Toteutuksen aloittaminen ja huomioon otettavat asiat

### 1. **Projektin perusrakenne**
Projektin hakemistorakenne on suunniteltu siten, että se tukee modulaarisuutta ja laajennettavuutta. 
Tämä helpottaa koodin ylläpitoa, testattavuutta ja skaalautuvuutta.

```
/SensorAPI
    /app
        ├── main.py           # Maini sovelluksen käynnistykseen, sisältää FastAPIn ja reitit
        ├── __init__.py       # Tyhjä tiedosto, joka tekee /app-hakemistosta Python-paketin
        ├── database/         # Databasen tiedostot
        │    ├── models.py    # SQLModelin/SQLAlchemyn tietokantaa varten luokat
        │    ├── database.py  # Yhteys SQLite tietokantaan
        │    ├── schemas.py   # Pydantic-mallit datan validointiin (saattaa muuttua)
        │    ├── crud.py      # Tietokantakyselyt ja funktiot (saatan tehdä useamman crudin jaettuna eri toiminnoille)
        │    ├── __init__.py  # Mahdollistaa /database-hakemiston moduulina käytön
        │
        ├── routes/           # APIRouter tiedostot ja toiminnallisuudet
        │   ├── sensors.py    # Anturien hallinta
        │   ├── blocks.py     # Lohkojen hallinta
        │   ├── readings.py   # Mittarien hallinta
        │   ├── status.py     # Tilahistorian hallinta
        │   ├── __init__.py   # Mahdollistaa /routes-hakemiston moduulina käytön
        │
        ├── dependencies.py   # Riippuvuuksien injektointi (katsotaan pidänkö tätä, teoria kiinnostaa)
        │
    /tests                    # Testitiedostot, katsotaan teenko mitään erillisiä, mutta ainakin teoriassa
        ├── test_sensors.py   # Anturitestit
        ├── test_blocks.py    # Lohkotestit
        ├── test_readings.py  # Mittaustestit
        ├── __init__.py       # Mahdollistaa /tests-hakemiston moduulina käytön
        │
    /docs                     # Dokumentaatiot
    ├── README.md             # Yleiskuvaus, suunnitelma ja käyttöohjeet
    ├── requirements.txt      # Tarvittavat riippuvuudet / paketit
```

#### **Perustelut:**
- **Modulaarinen rakenne**: API-routet, tietokanta ja liiketoimintalogiikka pidetään erillään, jotta sovelluksen osia voidaan muokata ilman suurta vaikutusta muihin osiin.
- **Eri tiedostot eri toiminnoille**: `routes/` sisältää API-routet, `models.py` määrittelee tietokantarakenteen, ja `schemas.py` hallitsee datan validoinnin. (Katsotaan onnistunko)
- **Helpompi testattavuus**: Testit pidetään erillisessä `/tests/`-hakemistossa, mikä mahdollistaa eristetyt yksikkötestit ja integrointitestit. (Ei välttämättä säily lopulliseen toteutukseen, mutta teoriassa kiinnostava.)
Tämä on alustava rakenne ja voi muuttua matkan varrella.

### 2. **Tietokannan suunnittelu**

Suunnittelin tietokannan taulut vastaamaan tehtävänannon vaatimuksia ja tukemaan tehokasta tietokantakyselyiden suorittamista. En ole aikaisemmin toteuttanut vastaavaa ratkaisua, joten mielenkiitoista nähdä onko tämä oikea ja järkevä ratkaisu.

- **`blocks`**:               Sisältää tehdashallin lohkot, joihin anturit sijoitetaan.
- **`sensors`**:              Hallitsee anturit, niiden identiteetin, sijainnin ja tilan.
- **`temperature_readings`**: Tallentaa lämpötilamittaukset ajan kanssa.
- **`sensor_status`**:        Kirjaa ylös kaikki tilamuutokset, mikä mahdollistaa virhelokituksen.

#### **Perustelut:**
- **Normalisoitu rakenne**:   Taulut on jaettu erillisiin yksiköihin, jotta tietojen haku on tehokasta ja data ei ole redundanttia.
- **Tilanseuranta**:          `temperature_readings` ja `sensor_status` mahdollistavat tietojen historian tarkastelun ilman datan ylikirjoittamista (ainakin teoriassa).

### 3. **API-routejen suunnittelu**

API-routet jaetaan loogisiin kokonaisuuksiin `routes/`-hakemistoon. Voi olla, että lopullisessa työssä teen tämän eri tavalla.

- **sensors.py**:             Anturien CRUD-toiminnot ja tilan muokkaus.
- **blocks.py**:              Lohkojen CRUD-toiminnot.
- **readings.py**:            Lämpötilamittausten käsittely.
- **status.py**:              Anturien tilahistorian hallinta.

#### **Perustelut:**
- **Eri tiedostot eri resursseille**: Anturit, lohkot ja mittaukset hallitaan erikseen, mikä selkeyttää ylläpitoa.
- **Yksinkertaistaa ylläpitoa ja laajennettavuutta**: Tulevien/mahdollisten uusien ominaisuuksien lisääminen ei vaadi suuria muutoksia koko koodipohjaan.

### 4. **Virheenkäsittely**

Virheenkäsittelyssä käytetään:

- **Pydanticin skeemat** datan validointiin (`schemas.py`).
- **FastAPI:n `HTTPException`** selkeiden virheilmoitusten antamiseen.
- **Lokitus**, jotta ongelmat voidaan jäljittää myöhemmin.

#### **Esimerkki virheenkäsittelystä:**
```python
from fastapi import HTTPException

    if len(asd) == 0:
        raise HTTPException(
            status_code=404, detail=f"Sensor with the id: {sensor_id} was not found."
        )
```

#### **Perustelut:**
- **Parantaa API:n luotettavuutta**: Varmistaa, että virhetilanteet käsitellään hallitusti.
- **Helpottaa debuggausta**: Hyvät virheilmoitukset auttavat ongelmien selvittämisessä.

---

## Käytetyt teknologiat / paketit
Projektissa käytetään samoja teknologioita/paketteja kuin kurssin aikana:

- **FastAPI**:    Python-web-framework REST API:n toteutukseen
- **SQLite**:     Kevyt tietokantaratkaisu
- **SQLAlchemy**: ORM, joka mahdollistaa tietokannan käytön ilman suoria SQL-kyselyitä
- **Pydantic**:   Datan validointiin ja mallintamiseen

### Perustelut:
- **FastAPI**:    Nopeus, helppokäyttöisyys ja automaattinen dokumentaatio.
- **SQLite**:     Kevyt ja erillistä tietokantapalvelinta ei tarvita.
- **SQLAlchemy**: Ylläpidettävyyden ja kehityksen helpottamiseksi.
- **Pydantic**:   Varmistaa datan oikeellisuuden API:ssa.

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
Tehtävänantona oli, että on 3kpl lohkoja, joiden sisällä on 2x2 ja 1x3 antureita ja antureilla on tiettyjä toimintoja. Tällöin oli loogista:
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