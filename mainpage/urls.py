from django.urls import path
from .views import home

app_name = "mainpage"

urlpatterns = [
    path("", home, name="home"),
]