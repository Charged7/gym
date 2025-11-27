# elevix/forms.py
from django import forms
from .models import GymUser


class ProfileEditForm(forms.ModelForm):
    """Форма редагування профілю"""

    class Meta:
        model = GymUser
        fields = ['first_name', 'last_name', 'middle_name', 'phone', 'age', 'gender', 'avatar', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True