from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import GymUser, Trainer


# --- Форма создания пользователя ---
class GymUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Підтвердження паролю", widget=forms.PasswordInput)

    class Meta:
        model = GymUser
        fields = ("email", "full_name", "phone", "age", "gender")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Паролі не співпадають.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # <<< хеширование тут
        if commit:
            user.save()
        return user


# --- Форма редактирования пользователя ---
class GymUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = GymUser
        fields = ("email", "full_name", "phone", "age", "gender", "password", "is_active", "is_staff")

    def clean_password(self):
        # Django требует вернуть исходный пароль (даже если он хэш)
        return self.initial["password"]


# --- Сам админ-класс ---
class GymUserAdmin(BaseUserAdmin):
    add_form = GymUserCreationForm
    form = GymUserChangeForm
    model = GymUser

    list_display = ("email", "full_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Особиста інформація", {"fields": ("full_name", "phone", "age", "gender")}),
        ("Права доступу", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "phone", "age", "gender", "password1", "password2", "is_active", "is_staff")}
        ),
    )


# Регистрируем
admin.site.register(GymUser, GymUserAdmin)

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "age", "gender", "experience")
    search_fields = ("full_name",)
