from django.urls import path
from .views import get_weather

app_name = "weather"

urlpatterns = [
    path("", get_weather, name="get_weather"),
]