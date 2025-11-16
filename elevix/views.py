import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from mysite.settings import BASE_DIR

from .forms import GymUserRegisterForm, LoginForm
from .models import GymUser

def index(request):
    return render(request, "elevix/index.html",)

def users(request):
    return render(request, "elevix/users.html",)

def trener_shablon(request):
    return render(request, "elevix/trener_shablon.html",)

def trener_cabinet(request):
    return render(request, "elevix/trener_cabinet.html",)

def trener_edit(request):
    return render(request, "elevix/trener_edit.html",)


def login(request):
    """Авторизация через форму с встроенной валидацией"""
    if request.method == "POST":
        form = LoginForm(request.POST, request=request)
        if form.is_valid():
            user = form.cleaned_data.get("user")
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Якщо користувач не обрав "запам’ятати мене" → сесія закінчиться після закриття браузера
            if not form.cleaned_data.get("remember"):
                request.session.set_expiry(0)

            messages.success(request, f"Вітаємо, {user.full_name}!")
            return redirect("user_profile")
        else:
            messages.error(request, "Помилка авторизації. Перевірте введені дані.")
    else:
        form = LoginForm()

    return render(request, "elevix/login.html", {"form": form})

logger = logging.getLogger("elevix")  # ← вот этот импорт

def register_gym_user(request):
    """Регистрация с автоматическим хешированием пароля"""

    if request.method == "POST":
        form = GymUserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            user = form.save(commit=False)
            # set_password автоматически хеширует пароль
            user.set_password(form.cleaned_data['password'])
            user.save()

            logger.info(f"Нова реєстрація: {email}")
            messages.success(request, "Реєстрація успішна!")
            return redirect("login")
        else:
            messages.error(request, "Виправте помилки у формі.")
    else:
        form = GymUserRegisterForm()

    return render(request, "elevix/register.html", {"form": form})


@login_required(login_url='login')
def user_profile(request):
    """Профиль пользователя с защитой авторизации"""
    user = request.user
    return render(request, "elevix/user_profile.html", {"user": user})

def logout_view(request):
    """Выход из системы"""
    auth_logout(request)
    messages.success(request, "Ви успішно вийшли з системи.")
    return redirect("login")

# -------------------------------
def reset_password_request(request):
    return render(request, "elevix/reset_password_request.html",)
