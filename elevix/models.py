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


class Trainer(models.Model):
    """Тренер спортзалу"""

    GENDER_CHOICES = [
        ('M', 'Чоловік'),
        ('F', 'Жінка'),
    ]

    SPECIALIZATION_CHOICES = [
        ('mma', 'ММА'),
        ('boxing', 'Бокс'),
        ('massage', 'Масаж'),
        ('fitness', 'Фітнес'),
        ('yoga', 'Йога'),
        ('crossfit', 'Кросфіт'),
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


class Service(models.Model):
    """Послуги залу"""

    CATEGORY_CHOICES = [
        ('group_training', 'Групове тренування'),
        ('personal_training', 'Персональне тренування'),
        ('massage', 'Масаж'),
    ]

    name = models.CharField("Назва послуги", max_length=200)
    description = models.TextField("Опис", blank=True)
    duration = models.DecimalField("Тривалість (години)", max_digits=4, decimal_places=2)
    category = models.CharField("Категорія", max_length=50, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField("Активна", default=True)

    # Додаткові поля для специфікації
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='services',
        verbose_name="Тренер"
    )

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    class Meta:
        db_table = 'services'
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class PricingPlan(models.Model):
    """Тарифні плани для послуг"""

    PLAN_TYPE_CHOICES = [
        ('single', 'Разове'),
        ('package', 'Пакет'),
    ]

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='pricing_plans',
        verbose_name="Послуга"
    )

    name = models.CharField("Назва плану", max_length=100)
    plan_type = models.CharField("Тип плану", max_length=20, choices=PLAN_TYPE_CHOICES)
    price = models.DecimalField("Ціна (грн)", max_digits=10, decimal_places=2)
    sessions_count = models.PositiveIntegerField(
        "Кількість занять",
        null=True,
        blank=True,
        help_text="Залиште порожнім для разового"
    )
    discount_percent = models.DecimalField(
        "Знижка (%)",
        max_digits=5,
        decimal_places=2,
        default=0,
        blank=True
    )
    is_default = models.BooleanField("Базовий план", default=False)

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    class Meta:
        db_table = 'pricing_plans'
        verbose_name = 'Тарифний план'
        verbose_name_plural = 'Тарифні плани'
        ordering = ['service', 'price']

    def __str__(self):
        return f"{self.service.name} - {self.name} ({self.price} грн)"

    def get_price_per_session(self):
        """Ціна за одне заняття"""
        if self.sessions_count and self.sessions_count > 0:
            return self.price / self.sessions_count
        return self.price


class ServiceFeature(models.Model):
    """Особливості/переваги послуг"""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name="Послуга"
    )

    feature_text = models.CharField("Текст особливості", max_length=250)
    icon = models.CharField("Іконка", max_length=50, blank=True, help_text="Назва іконки або клас")
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        db_table = 'service_features'
        verbose_name = 'Особливість послуги'
        verbose_name_plural = 'Особливості послуг'
        ordering = ['service', 'sort_order']

    def __str__(self):
        return f"{self.service.name} - {self.feature_text[:50]}"


class Booking(models.Model):
    """Бронювання послуг"""

    STATUS_CHOICES = [
        ('pending', 'Очікує підтвердження'),
        ('confirmed', 'Підтверджено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(
        GymUser,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Користувач"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Послуга"
    )

    pricing_plan = models.ForeignKey(
        PricingPlan,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name="Тарифний план"
    )

    booking_date = models.DateTimeField("Дата та час бронювання")
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField("Загальна сума (грн)", max_digits=10, decimal_places=2)

    # Для пакетних послуг
    sessions_total = models.PositiveIntegerField("Всього занять", null=True, blank=True)
    sessions_remaining = models.PositiveIntegerField("Залишок занять", null=True, blank=True)

    # Додаткова інформація
    notes = models.TextField("Примітки", blank=True)

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Бронювання'
        verbose_name_plural = 'Бронювання'
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.service.name} ({self.booking_date.strftime('%d.%m.%Y')})"

    def save(self, *args, **kwargs):
        # Автоматично встановлюємо кількість занять при створенні
        if not self.pk and self.pricing_plan.sessions_count:
            self.sessions_total = self.pricing_plan.sessions_count
            self.sessions_remaining = self.pricing_plan.sessions_count
        super().save(*args, **kwargs)


class Schedule(models.Model):
    """Розклад тренувань"""

    WEEKDAY_CHOICES = [
        (0, 'Понеділок'),
        (1, 'Вівторок'),
        (2, 'Середа'),
        (3, 'Четвер'),
        (4, 'П\'ятниця'),
        (5, 'Субота'),
        (6, 'Неділя'),
    ]

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="Тренер"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name="Послуга"
    )

    day_of_week = models.PositiveSmallIntegerField("День тижня", choices=WEEKDAY_CHOICES)
    start_time = models.TimeField("Час початку")
    end_time = models.TimeField("Час закінчення")
    max_participants = models.PositiveIntegerField(
        "Макс. учасників",
        default=1,
        help_text="Для групових тренувань"
    )

    is_active = models.BooleanField("Активний", default=True)

    class Meta:
        db_table = 'schedules'
        verbose_name = 'Розклад'
        verbose_name_plural = 'Розклади'
        ordering = ['day_of_week', 'start_time']
        unique_together = ['trainer', 'day_of_week', 'start_time']

    def __str__(self):
        return f"{self.trainer.get_full_name()} - {self.get_day_of_week_display()} {self.start_time}"


class FAQ(models.Model):
    """Часті питання та відповіді"""

    question = models.CharField("Питання", max_length=500)
    answer = models.TextField("Відповідь")
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    is_active = models.BooleanField("Активне", default=True)

    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Дата оновлення", auto_now=True)

    class Meta:
        db_table = 'faqs'
        verbose_name = 'Питання (FAQ)'
        verbose_name_plural = 'Питання (FAQ)'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.question[:50]