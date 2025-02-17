from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.urls import reverse
from .forms import FavoriteCityForm
from .models import FavoriteCity
from django.shortcuts import get_object_or_404

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("mainpage:home"))  # Przekierowanie na stronę główną
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse("mainpage:home"))  # Przekierowanie na stronę główną
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse("mainpage:home"))  # Przekierowanie na stronę główną


@login_required
def add_favorite_city(request):
    if request.method == "POST":
        form = FavoriteCityForm(request.POST)
        if form.is_valid():
            favorite_city = form.save(commit=False)
            favorite_city.user = request.user
            favorite_city.save()
            return redirect("mainpage:home")
    else:
        form = FavoriteCityForm()

    return render(request, "accounts/add_favorite_city.html", {"form": form})

@login_required
def favorite_cities(request):
    cities = FavoriteCity.objects.filter(user=request.user)
    return render(request, "accounts/favorite_cities.html", {"cities": cities})



@login_required
def delete_favorite_city(request, city_id):
    city = get_object_or_404(FavoriteCity, id=city_id, user=request.user)
    city.delete()
    return redirect("accounts:favorite_cities")