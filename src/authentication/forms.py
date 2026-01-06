from django import forms
from allauth.account.forms import SignupForm
from phonenumber_field.formfields import PhoneNumberField
from src.elevix.models import GymUser


class CustomSignupForm(SignupForm):
    """Кастомна форма реєстрації для GymUser"""

    first_name = forms.CharField(
        max_length=100,
        label="Ім'я",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Іван",
            'autocomplete': 'given-name',
        })
    )

    last_name = forms.CharField(
        max_length=100,
        label="Прізвище",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Іваненко',
            'autocomplete': 'family-name',
        })
    )

    middle_name = forms.CharField(
        max_length=100,
        label="По-батькові",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Іванович (необов\'язково)',
            'autocomplete': 'additional-name',
        })
    )

    phone = PhoneNumberField(
        region="UA",
        label="Телефон",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380501234567',
            'autocomplete': 'tel',
        })
    )

    age = forms.IntegerField(
        label="Вік",
        min_value=14,
        max_value=120,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '25',
        })
    )

    gender = forms.ChoiceField(
        choices=[('', '--- Оберіть ---')] + GymUser.GENDER_CHOICES,
        label="Стать",
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

    # ⚠️ ВАЖЛИВО: Перевизначаємо email без username
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Прибираємо username field (якщо є)
        if 'username' in self.fields:
            del self.fields['username']

        # Кастомізуємо email
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'example@gmail.com',
            'autocomplete': 'email',
        })

    def save(self, request):
        """Зберігаємо користувача з усіма полями"""
        user = super().save(request)

        # Зберігаємо додаткові поля
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.middle_name = self.cleaned_data.get('middle_name', '')
        user.phone = self.cleaned_data.get('phone')
        user.age = self.cleaned_data.get('age')
        user.gender = self.cleaned_data.get('gender', '')

        user.save()
        return user
