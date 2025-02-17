from django.urls import path
from .views import register_view, login_view, logout_view
from .views import add_favorite_city, favorite_cities
from .views import delete_favorite_city

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("favorite-cities/", favorite_cities, name="favorite_cities"),
    path("add-favorite-city/", add_favorite_city, name="add_favorite_city"),
    path("delete-favorite-city/<int:city_id>/", delete_favorite_city, name="delete_favorite_city"),
]