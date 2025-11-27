from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(DjangoUserManager):
    """Кастомний менеджер для користувача без username"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email є обов\'язковим')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser повинен мати is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser повинен мати is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class GymUser(AbstractUser):
    """Користувач спортзалу"""

    # Прибираємо username - використовуємо email
    username = None

    objects = CustomUserManager()

    # ПІБ (окремі поля)
    first_name = models.CharField("Ім'я", max_length=100)
    last_name = models.CharField("Прізвище", max_length=100)
    middle_name = models.CharField("По-батькові", max_length=100, blank=True)

    # Контакти
    email = models.EmailField("Email", unique=True)
    phone = PhoneNumberField("Телефон", region="UA", blank=True, null=True)

    # Додаткова інформація
    age = models.PositiveIntegerField("Вік", blank=True, null=True)

    GENDER_CHOICES = [
        ('M', 'Чоловік'),
        ('F', 'Жінка'),
        ('O', 'Інше'),
    ]
    gender = models.CharField("Стать", max_length=1, choices=GENDER_CHOICES, blank=True)

    # Аватар (опціонально)
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True, null=True)

    # Про себе
    bio = models.TextField("Про себе", max_length=500, blank=True)

    # Налаштування
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = 'gym_users'
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def get_full_name(self):
        """Прізвище Ім'я По-батькові"""
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(filter(None, parts))

    def get_short_name(self):
        """Прізвище І.П."""
        initials = f"{self.first_name[0]}."
        if self.middle_name:
            initials += f"{self.middle_name[0]}."
        return f"{self.last_name} {initials}"


# models.py
class Trainer(models.Model):
    """Тренер спортзалу"""

    GENDER_CHOICES = [
        ('M', 'Чоловік'),
        ('F', 'Жінка'),
    ]

    SPECIALIZATION_CHOICES = [
        ('fitness', 'Фітнес'),
        ('yoga', 'Йога'),
        ('boxing', 'Бокс'),
        ('crossfit', 'Кросфіт'),
        ('swimming', 'Плавання'),
        ('pilates', 'Пілатес'),
    ]

    user = models.OneToOneField(
        GymUser,
        on_delete=models.CASCADE,
        related_name='trainer_profile',
        verbose_name="Користувач",
        blank=True,
        null=True
    )

    first_name = models.CharField("Ім'я", max_length=100)
    last_name = models.CharField("Прізвище", max_length=100)
    middle_name = models.CharField("По-батькові", max_length=100, blank=True)

    age = models.PositiveIntegerField("Вік")
    gender = models.CharField("Стать", max_length=1, choices=GENDER_CHOICES)
    experience = models.PositiveIntegerField("Стаж (років)")
    specialization = models.CharField(
        "Спеціалізація",
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        default='fitness'
    )

    photo = models.ImageField("Фото", upload_to='trainers/', blank=True, null=True)
    description = models.TextField("Опис", blank=True)

    # Нові поля з вашого JSON
    graduate = models.TextField("Освіта", blank=True)
    work_experience = models.TextField("Досвід роботи", blank=True)

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    class Meta:
        db_table = 'trainers'
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренери'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_specialization_display()}"

    def get_full_name(self):
        """Повне ім'я"""
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(filter(None, parts))