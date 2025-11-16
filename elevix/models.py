from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class Trainer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]

    full_name = models.CharField("ФИО", max_length=100)
    age = models.PositiveIntegerField("Возраст")
    gender = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES)
    experience = models.PositiveIntegerField("Стаж работы (лет)")

    def __str__(self):
        return f"{self.full_name} ({self.get_gender_display()})"


class GymUserManager(BaseUserManager):
    """Менеджер для кастомной модели пользователя"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not password:
            raise ValueError("Пароль обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Автоматически хеширует пароль
        user.is_active = extra_fields.get("is_active", True)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class GymUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField("ФІО", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone = PhoneNumberField("Телефон", region="UA", unique=True, blank=True, null=True)
    age = models.PositiveIntegerField("Вік", null=True, blank=True)
    gender = models.CharField(
        "Стать",
        max_length=10,
        choices=[("M", "Чоловік"), ("F", "Жінка")],
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = GymUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"
