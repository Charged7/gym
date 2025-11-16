from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from .models import GymUser

class GymUserRegisterForm(forms.ModelForm):
    phone = PhoneNumberField(
        region="UA",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380XXXXXXXXX',
            'autocomplete': 'tel',
        }),
        label="Телефон"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль',
            'autocomplete': 'new-password',
        }),
        label="Пароль",
        help_text="Мінімум 8 символів, не тільки цифри"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть пароль',
            'autocomplete': 'new-password',
        }),
        label="Підтвердження паролю"
    )

    class Meta:
        model = GymUser
        fields = ["full_name", "email", "phone", 'age', 'gender']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ПІБ',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'autocomplete': 'email',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вік',
                'min': 16,
                'max': 100,
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if GymUser.objects.filter(email=email).exists():
            raise ValidationError("Користувач з таким email вже існує.")
        return email

    def clean_password(self):
        """Валидация пароля по правилам Django"""
        password = self.cleaned_data.get('password')
        if password:
            try:
                validate_password(password)  # Используем встроенную валидацию Django
            except ValidationError as e:
                raise ValidationError("Пароль надто простий або занадто короткий.")
        return password

    def clean(self):
        """Проверка совпадения паролей"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError({
                'password_confirm': "Паролі не співпадають."
            })

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Введіть email",
            "autocomplete": "email",
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Введіть пароль",
            "autocomplete": "current-password",
        })
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """Валідація та автентифікація користувача"""
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(self.request, username=email, password=password)
            if user is None:
                raise ValidationError("Невірний email або пароль.")
            if not user.is_active:
                raise ValidationError("Цей акаунт деактивовано.")

            # Добавляем пользователя в cleaned_data
            cleaned_data["user"] = user

        return cleaned_data