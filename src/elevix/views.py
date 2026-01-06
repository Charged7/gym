from decouple import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ProfileEditForm
from .models import Trainer, Service, FAQ


def index(request):
    """Головна сторінка з тренерами та послугами"""
    trainers = Trainer.objects.all()
    services = Service.objects.filter(
        is_active=True
    ).prefetch_related(
        'pricing_plans',
        'features'
    ).order_by('id')

    faqs = FAQ.objects.filter(is_active=True).order_by('sort_order', 'id')

    return render(request, "index.html", {
        "trainers": trainers,
        "services": services,
        "faqs": faqs,
    })


def trainers_list(request):
    """Список всіх тренерів"""
    trainers = Trainer.objects.all()
    print(f"Кількість тренерів: {trainers.count()}")
    return render(request, 'elevix/trainers_list.html', {'trainers': trainers})


def trainer_detail(request, pk):
    """Детальна сторінка тренера"""
    trainer = get_object_or_404(Trainer, pk=pk)

    # Отримуємо послуги цього тренера
    services = trainer.services.filter(is_active=True)

    # Отримуємо розклад цього тренера
    schedules = trainer.schedules.filter(is_active=True).order_by('day_of_week', 'start_time')

    context = {
        'trainer': trainer,
        'services': services,
        'schedules': schedules,
    }
    return render(request, 'elevix/trainer_detail.html', context)


@login_required(login_url='account_login')
def profile(request):
    """Профіль користувача з захистом авторизації"""
    user = request.user
    return render(request, "elevix/profile.html", {"user": user})


@login_required(login_url='account_login')
def profile_edit(request):
    """Редагування профілю"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль успішно оновлено!')
            return redirect('elevix:profile')
    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'elevix/profile_edit.html', {'form': form, 'user': request.user})


def logout_view(request):
    """Вихід із системи"""
    auth_logout(request)
    messages.success(request, "Ви успішно вийшли з системи.")
    return redirect("account_login")


@login_required(login_url='account_login')
def booking_create(request, service_id):
    """Створення бронювання послуги"""
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    # Тут буде логіка створення бронювання
    return render(request, 'elevix/booking_create.html', {'service': service})


def env_test_view(request):
    if not settings.DEBUG:
        return JsonResponse({'error': 'This view is only available in DEBUG mode.'})

    return JsonResponse({
        "EMAIL_HOST_USER": config("EMAIL_HOST_USER"),
        "DEBUG_MODE": settings.DEBUG,
        "SECRET_KEY_FIRST_5": config("SECRET_KEY")[:5] + "*****",
    })
