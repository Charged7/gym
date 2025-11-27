from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import GymUser, Trainer


@admin.register(GymUser)
class GymUserAdmin(UserAdmin):
    """Адмін панель для GymUser"""

    # Поля які показуються в списку
    list_display = (
        'email',
        'get_full_name_display',
        'phone',
        'age',
        'gender_display',
        'is_staff',
        'is_active',
        'date_joined',
    )

    # Фільтри збоку
    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'gender',
        'date_joined',
    )

    # Пошук
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'middle_name',
        'phone',
    )

    # Сортування за замовчуванням
    ordering = ('-date_joined',)

    # Поля для перегляду/редагування
    fieldsets = (
        ('🔐 Автентифікація', {
            'fields': ('email', 'password')
        }),
        ('👤 Персональна інформація', {
            'fields': (
                ('first_name', 'last_name'),
                'middle_name',
                'phone',
                ('age', 'gender'),
                'avatar',
                'bio',
            )
        }),
        ('🔑 Права доступу', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
            'classes': ('collapse',),
        }),
        ('📅 Важливі дати', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )

    # Поля при створенні нового користувача
    add_fieldsets = (
        ('🔐 Створення користувача', {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'middle_name',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )

    # Кастомні методи для відображення
    @admin.display(description='ПІБ', ordering='last_name')
    def get_full_name_display(self, obj):
        """Відображення повного імені"""
        return obj.get_full_name() or '—'

    @admin.display(description='Стать')
    def gender_display(self, obj):
        """Відображення статі з іконками"""
        icons = {
            'M': '👨',
            'F': '👩',
            'O': '⚧️',
        }
        gender_text = obj.get_gender_display() if obj.gender else '—'
        icon = icons.get(obj.gender, '')
        return format_html('{} {}', icon, gender_text)

    # Доступ до username видалено
    def get_fieldsets(self, request, obj=None):
        """Видаляємо username з fieldsets"""
        fieldsets = super().get_fieldsets(request, obj)
        return fieldsets

    actions = ['activate_users', 'deactivate_users', 'send_email']

    @admin.action(description='✅ Активувати обраних користувачів')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активовано {updated} користувач(ів).')

    @admin.action(description='❌ Деактивувати обраних користувачів')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивовано {updated} користувач(ів).')


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    """Адмін панель для Trainer"""

    # Поля які показуються в списку
    list_display = (
        'get_photo_preview',
        'get_full_name',
        'age',
        'gender_display',
        'specialization_display',
        'experience',
        'user_link',
        'created_at',
    )

    # Фільтри збоку
    list_filter = (
        'gender',
        'specialization',
        'experience',
        'created_at',
    )

    # Пошук
    search_fields = (
        'first_name',
        'last_name',
        'description',
        'user__email',
    )

    # Сортування за замовчуванням
    ordering = ('-created_at',)

    # Поля для редагування
    fieldsets = (
        ('👤 Основна інформація', {
            'fields': (
                ('first_name', 'last_name'),
                ('age', 'gender'),
                'photo',
            )
        }),
        ('💼 Професійна інформація', {
            'fields': (
                'specialization',
                'experience',
                'description',
            )
        }),
        ('🔗 Зв\'язок з користувачем', {
            'fields': ('user',),
            'classes': ('collapse',),
        }),
    )

    # Поля тільки для читання
    readonly_fields = ('created_at', 'updated_at')

    # Автозаповнення для ForeignKey
    autocomplete_fields = ['user']

    # Кастомні методи
    @admin.display(description='Фото')
    def get_photo_preview(self, obj):
        """Попередній перегляд фото"""
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />',
                obj.photo.url
            )
        return '—'

    @admin.display(description='ПІБ', ordering='last_name')
    def get_full_name(self, obj):
        """Відображення ПІБ"""
        return obj.get_full_name()

    @admin.display(description='Стать')
    def gender_display(self, obj):
        """Відображення статі з іконками"""
        icons = {'M': '👨', 'F': '👩'}
        icon = icons.get(obj.gender, '')
        return format_html('{} {}', icon, obj.get_gender_display())

    @admin.display(description='Спеціалізація')
    def specialization_display(self, obj):
        """Відображення спеціалізації з емодзі"""
        emojis = {
            'fitness': '💪',
            'yoga': '🧘',
            'boxing': '🥊',
            'crossfit': '🏋️',
            'swimming': '🏊',
            'pilates': '🤸',
        }
        emoji = emojis.get(obj.specialization, '')
        return format_html('{} {}', emoji, obj.get_specialization_display())

    @admin.display(description='Користувач')
    def user_link(self, obj):
        """Посилання на користувача"""
        if obj.user:
            url = f"/admin/elevix/gymuser/{obj.user.pk}/change/"
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.user.email
            )
        return '—'

    # Дії
    actions = ['make_active', 'export_trainers']

    @admin.action(description='Експортувати обраних тренерів')
    def export_trainers(self, request, queryset):
        """Експорт тренерів (приклад)"""
        count = queryset.count()
        self.message_user(
            request,
            f'Експортовано {count} тренер(ів).'
        )


# Налаштування заголовків адмін панелі
admin.site.site_header = "Elevix - Адміністрування"
admin.site.site_title = "Elevix Admin"
admin.site.index_title = "Панель керування спортзалом"
