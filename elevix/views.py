import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import ProfileEditForm
from .models import Trainer

def index(request):
    trainers = Trainer.objects.all()
    return render(request, "index.html", {"trainers": trainers})

def trainers_list(request):
    """Список всіх тренерів"""
    trainers = Trainer.objects.all()
    print(f"Кількість тренерів: {trainers.count()}")
    return render(request, 'elevix/trainers_list.html', {'trainers': trainers})

def trainer_detail(request, pk):
    """Детальна сторінка тренера"""
    trainer = get_object_or_404(Trainer, pk=pk)
    return render(request, 'elevix/trainer_detail.html', {'trainer': trainer})

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