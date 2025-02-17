import requests
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime


# Lista poprawnych województw do filtrowania wyników
WOJEWODZTWA = [
    "Dolnośląskie", "Kujawsko-Pomorskie", "Lubelskie", "Lubuskie",
    "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie",
    "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
    "Świętokrzyskie", "Warmińsko-Mazurskie", "Wielkopolskie", "Zachodniopomorskie"
]


# Mapowanie kodów pogodowych na opisy tekstowe
WEATHER_DESCRIPTIONS = {
    0: "Słonecznie",
    1: "Głównie słonecznie",
    2: "Częściowe zachmurzenie",
    3: "Pochmurno",
    45: "Mgła",
    48: "Osadzająca się mgła",
    51: "Lekka mżawka",
    53: "Mżawka",
    55: "Gęsta mżawka",
    61: "Lekki deszcz",
    63: "Deszcz",
    65: "Ulewa",
    80: "Przelotny deszcz",
    81: "Mocny przelotny deszcz",
    82: "Bardzo mocny przelotny deszcz",
    95: "Burza",
    96: "Burza z deszczem",
    99: "Burza z gradem",
}

# Mapowanie dni tygodnia na język polski
DAYS_PL = {
    "Monday": "Poniedziałek",
    "Tuesday": "Wtorek",
    "Wednesday": "Środa",
    "Thursday": "Czwartek",
    "Friday": "Piątek",
    "Saturday": "Sobota",
    "Sunday": "Niedziela",
}

# Mapowanie kodów pogodowych na emoji ikonki
WEATHER_ICONS = {
    0: "☀️",  # Słonecznie
    1: "🌤️",  # Głównie słonecznie
    2: "⛅",  # Częściowe zachmurzenie
    3: "☁️",  # Pochmurno
    45: "🌫️",  # Mgła
    48: "🌫️",  # Osadzająca się mgła
    51: "🌦️",  # Lekka mżawka
    53: "🌧️",  # Mżawka
    55: "🌧️",  # Gęsta mżawka
    61: "🌦️",  # Lekki deszcz
    63: "🌧️",  # Deszcz
    65: "🌧️",  # Ulewa
    80: "🌦️",  # Przelotny deszcz
    81: "🌧️",  # Mocny przelotny deszcz
    82: "⛈️",  # Bardzo mocny przelotny deszcz
    95: "⛈️",  # Burza
    96: "⛈️",  # Burza z deszczem
    99: "⛈️",  # Burza z gradem
}

def format_location(geo_data):
    display_name = geo_data.get("display_name", "")
    parts = display_name.split(", ")

    if len(parts) < 2:
        return "Nieznana lokalizacja"

    # Spróbuj znaleźć nazwę miasta
    city = parts[0]  # Najczęściej pierwsza część to miasto
    country = parts[-1]  # Kraj to ostatnia część

    return f"{city}, {country}"

def get_weather(request):
    """Pobiera i przetwarza dane pogodowe dla podanego miasta"""
    city = None

    # Sprawdź, czy miasto zostało przekazane przez GET (link) lub POST (formularz)
    if request.method == "GET":
        city = request.GET.get("city")
    elif request.method == "POST":
        city = request.POST.get("city")

    if city:
        # Pobieramy współrzędne geograficzne miasta z OpenStreetMap
        headers = {"User-Agent": "WeatherApp/1.0 (your@email.com)"}  # Podaj swój e-mail!
        geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
        geo_response = requests.get(geo_url, headers=headers)

        print(f"STATUS CODE: {geo_response.status_code}")  # Sprawdź kod odpowiedzi
        print(f"RESPONSE TEXT: {geo_response.text}")  # Zobacz całą odpowiedź

        try:
            geo_data = geo_response.json()
            if not geo_data:  # Jeśli pusty JSON
                messages.error(request, "Brak danych dla tego miasta.")
                return render(request, "weather/index.html")
        except requests.exceptions.JSONDecodeError:
            messages.error(request, "Błąd pobierania lokalizacji.")
            return render(request, "weather/index.html")

        if not geo_data:
            messages.error(request, "Nie znaleziono lokalizacji.")
            return render(request, "weather/index.html")

        # Upewnijmy się, że mamy poprawny wynik
        first_result = geo_data[0]
        print(f"First result: {first_result}")  # Dodajemy to debugowanie

        # Pobieramy dane o lokalizacji
        location_name = format_location(first_result)

        lat = first_result["lat"]
        lon = first_result["lon"]

        # Pobieramy dane pogodowe
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&hourly=temperature_2m,relative_humidity_2m,windspeed_10m"
            "&daily=weathercode,temperature_2m_min,temperature_2m_max,precipitation_probability_max"
            "&timezone=Europe/Warsaw"
        )

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if "hourly" not in weather_data or "daily" not in weather_data:
            messages.error(request, "Nie udało się pobrać danych pogodowych.")
            return render(request, "weather/index.html")

        # Pobieramy temperatury godzinowe i przypisujemy je do dni
        hourly_temps = [weather_data["hourly"]["temperature_2m"][i * 24:(i + 1) * 24] for i in range(7)]
        hours = [f"{i}:00" for i in range(24)]

        # Dane dla prognozy tygodniowej
        weather = [
            {
                "date": weather_data["daily"]["time"][i],
                "temp_min": weather_data["daily"]["temperature_2m_min"][i],
                "temp_max": weather_data["daily"]["temperature_2m_max"][i],
                "icon": WEATHER_ICONS.get(weather_data["daily"]["weathercode"][i], "☁️"),  # Ikona dla każdego dnia
            }
            for i in range(7)
        ]




        # Pobieramy dzisiejszą datę z API
        current_date_str = weather_data["daily"]["time"][0]  # Format: 'YYYY-MM-DD'
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")

        # Konwertujemy na nazwę dnia tygodnia
        weekday_name = current_date.strftime("%A")  # np. 'Monday'

        # Pobieramy dzisiejszą datę z API
        current_date_str = weather_data["daily"]["time"][0]  # Format: 'YYYY-MM-DD'
        current_date = datetime.strptime(current_date_str, "%Y-%m-%d")

        # Pobieramy angielską nazwę dnia tygodnia i tłumaczymy na polski
        weekday_name = current_date.strftime("%A")  # np. 'Monday'
        weekday_name_pl = DAYS_PL.get(weekday_name, weekday_name)  # Pobiera polski odpowiednik



        context = {
            "location_name": location_name,
            "current_weather": {
                "temp": weather_data["daily"]["temperature_2m_max"][0],  # Maksymalna temp. dzisiejsza
                "humidity": weather_data["hourly"]["relative_humidity_2m"][0],  # Wilgotność
                "wind_speed": weather_data["hourly"]["windspeed_10m"][0],  # Wiatr
                "precipitation": weather_data["daily"]["precipitation_probability_max"][0],  # Szansa na opady
                "weekday": weekday_name_pl,  # pl dzień tygodnia
                "date": current_date.strftime("%d.%m.%Y"),  # Format 'DD.MM.YYYY'
                "description": "Aktualna pogoda",
            },
            "weather": weather,
            "hourly_temps": hourly_temps,
            "hours": hours,
        }

        # Pobieramy kod pogody i dodajemy opis
        weather_code = weather_data["daily"]["weathercode"][0]
        weather_description = WEATHER_DESCRIPTIONS.get(weather_code, "Nieznana pogoda")
        context["current_weather"]["description"] = weather_description

        # Pobieramy kod pogody i dodajemy ikonę
        weather_code = weather_data["daily"]["weathercode"][0]
        weather_icon = WEATHER_ICONS.get(weather_code, "☁️")  # Domyślnie ❓ gdykodu

        context["current_weather"]["icon"] = weather_icon  # Dodajemy ikonę do kontekstu

        return render(request, "weather/index.html", context)

    # Jeśli nie przekazano miasta, wyświetl pustą stronę
    return render(request, "weather/index.html")