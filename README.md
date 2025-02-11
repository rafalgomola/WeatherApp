# WeatherApp – Aplikacja pogodowa

WeatherApp to aplikacja webowa napisana w Pythonie we frameworku Django, umożliwiająca sprawdzanie prognozy pogody dla dowolnego miasta.  
Użytkownicy mogą rejestrować się, logować oraz zapisywać swoje ulubione miasta.  

Dane pogodowe pochodzą z opensource'owego API [Open-Meteo] (https://open-meteo.com/).  
Wykres temperatury godzinowej generowany jest przy użyciu  [Chart.js] (https://www.chartjs.org/).  

## Instalacja i uruchomienie

Aby uruchomić aplikację lokalnie, wykonaj poniższe kroki.

### 1. Klonowanie repozytorium
Najpierw pobierz kod z GitHuba:

```bash
git clone https://github.com/TWOJ-NICK/WeatherApp.git
cd WeatherApp
```

**### 2. Tworzenie wirtualnego środowiska i instalacja zależności**

```
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

**### 3. Wykonanie migracji bazy danych**

```
python manage.py migrate
```

**### 4. Uruchomienie serwera**
```
python manage.py runserver
```

