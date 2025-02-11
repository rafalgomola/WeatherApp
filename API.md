# Dokumentacja API WeatherApp

WeatherApp udostępnia publiczne API do pobierania danych pogodowych.

## 1. Pobranie prognozy pogody dla miasta

- **URL:**  
  ```plaintext
  /weather/?city=NazwaMiasta
  ```
- **Metoda: GET**

- **Parametry:**
  - city – nazwa miasta do wyszukania
Przykładowe zapytanie:
rzykładowe zapytanie:
```plaintext
GET /weather/?city=Gliwice
```
Przykładowa odpowiedź (JSON):


```plaintext
{
  "location_name": "Gliwice, Polska",
  "current_weather": {
    "temp": 10.2,
    "description": "Pogodnie"
  },
  "weather": [
    {"date": "2025-02-10", "temp_min": 5.0, "temp_max": 12.0},
    {"date": "2025-02-11", "temp_min": 3.0, "temp_max": 10.0}
  ]
}
```
Dane pogodowe pochodzą z API Open-Meteo.
Geolokalizacja miast realizowana przez OpenStreetMap.
