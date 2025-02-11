from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.urls import reverse

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