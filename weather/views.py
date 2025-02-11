import requests
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
# from .forms import RegisterForm, LoginForm

# Lista poprawnych województw do filtrowania wyników
WOJEWODZTWA = [
    "Dolnośląskie", "Kujawsko-Pomorskie", "Lubelskie", "Lubuskie",
    "Łódzkie", "Małopolskie", "Mazowieckie", "Opolskie",
    "Podkarpackie", "Podlaskie", "Pomorskie", "Śląskie",
    "Świętokrzyskie", "Warmińsko-Mazurskie", "Wielkopolskie", "Zachodniopomorskie"
]


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
    if request.method == "POST":
        city = request.POST.get("city")

        # Pobieramy współrzędne geograficzne miasta z OpenStreetMap
        headers = {"User-Agent": "WeatherApp/1.0 (your@email.com)"}  # Podaj swój e-mail!
        geo_url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json"
        geo_response = requests.get(geo_url, headers=headers)

        print(f"STATUS CODE: {geo_response.status_code}")  # Sprawdź kod odpowiedzi
        print(f"RESPONSE TEXT: {geo_response.text}")  # Zobacz całą odpowiedź

        try:
            geo_data = geo_response.json()
            if not geo_data:  # Jeśli pusty JSON
                raise ValueError("Brak danych dla tego miasta.")
        except requests.exceptions.JSONDecodeError:
            return render(request, "weather/index.html", {"error": "Błąd pobierania lokalizacji."})

        if not geo_data:
            return render(request, "weather/index.html", {"error": "Nie znaleziono lokalizacji."})

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
            "&hourly=temperature_2m&daily=weathercode,temperature_2m_min,temperature_2m_max"
            "&timezone=Europe/Warsaw"
        )

        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if "hourly" not in weather_data or "daily" not in weather_data:
            return render(request, "weather/index.html", {"error": "Nie udało się pobrać danych pogodowych."})

        # Pobieramy temperatury godzinowe i przypisujemy je do dni
        hourly_temps = [weather_data["hourly"]["temperature_2m"][i * 24:(i + 1) * 24] for i in range(7)]
        hours = [f"{i}:00" for i in range(24)]

        # Dane dla prognozy tygodniowej
        weather = [
            {
                "date": weather_data["daily"]["time"][i],
                "temp_min": weather_data["daily"]["temperature_2m_min"][i],
                "temp_max": weather_data["daily"]["temperature_2m_max"][i],
            }
            for i in range(7)
        ]

        context = {
            "location_name": location_name,
            "current_weather": {
                "temp": weather_data["daily"]["temperature_2m_max"][0],  # Obecna maksymalna temp.
                "description": "Aktualna pogoda",
            },
            "weather": weather,
            "hourly_temps": hourly_temps,
            "hours": hours,
        }

        return render(request, "weather/index.html", context)

    return render(request, "weather/index.html")