from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count, Sum
from .models import (
    GymUser,
    Trainer,
    Service,
    PricingPlan,
    ServiceFeature,
    Booking,
    Schedule,
    FAQ,
)


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

    actions = ['activate_users', 'deactivate_users']

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
                'middle_name',
                ('age', 'gender'),
                'photo',
            )
        }),
        ('💼 Професійна інформація', {
            'fields': (
                'specialization',
                'experience',
                'description',
                'graduate',
                'work_experience',
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
            'mma': '🥋',
            'boxing': '🥊',
            'massage': '💆',
            'fitness': '💪',
            'yoga': '🧘',
            'crossfit': '🏋️',
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
    actions = ['export_trainers']

    @admin.action(description='📊 Експортувати обраних тренерів')
    def export_trainers(self, request, queryset):
        """Експорт тренерів (приклад)"""
        count = queryset.count()
        self.message_user(
            request,
            f'Експортовано {count} тренер(ів).'
        )


class ServiceFeatureInline(admin.TabularInline):
    """Inline для особливостей послуг"""
    model = ServiceFeature
    extra = 1
    fields = ('feature_text', 'icon', 'sort_order')


class PricingPlanInline(admin.TabularInline):
    """Inline для тарифних планів"""
    model = PricingPlan
    extra = 1
    fields = ('name', 'plan_type', 'price', 'sessions_count', 'discount_percent', 'is_default')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Адмін панель для Service"""

    list_display = (
        'name',
        'category_display',
        'duration',
        'trainer_link',
        'is_active',
        'plans_count',
        'features_count',
        'created_at',
    )

    list_filter = (
        'category',
        'is_active',
        'created_at',
    )

    search_fields = (
        'name',
        'description',
        'trainer__first_name',
        'trainer__last_name',
    )

    ordering = ('category', 'name')

    fieldsets = (
        ('📋 Основна інформація', {
            'fields': (
                'name',
                'category',
                'description',
                'duration',
                'is_active',
            )
        }),
        ('👨‍🏫 Тренер', {
            'fields': ('trainer',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['trainer']

    inlines = [PricingPlanInline, ServiceFeatureInline]

    @admin.display(description='Категорія')
    def category_display(self, obj):
        """Відображення категорії з емодзі"""
        emojis = {
            'group_training': '👥',
            'personal_training': '👤',
            'massage': '💆',
        }
        emoji = emojis.get(obj.category, '')
        return format_html('{} {}', emoji, obj.get_category_display())

    @admin.display(description='Тренер')
    def trainer_link(self, obj):
        """Посилання на тренера"""
        if obj.trainer:
            url = f"/admin/elevix/trainer/{obj.trainer.pk}/change/"
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.trainer.get_full_name()
            )
        return '—'

    @admin.display(description='Тарифів')
    def plans_count(self, obj):
        """Кількість тарифних планів"""
        count = obj.pricing_plans.count()
        return format_html('<span style="color: blue;">📊 {}</span>', count)

    @admin.display(description='Особливостей')
    def features_count(self, obj):
        """Кількість особливостей"""
        count = obj.features.count()
        return format_html('<span style="color: green;">✅ {}</span>', count)

    actions = ['activate_services', 'deactivate_services']

    @admin.action(description='✅ Активувати обрані послуги')
    def activate_services(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активовано {updated} послуг(и).')

    @admin.action(description='❌ Деактивувати обрані послуги')
    def deactivate_services(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивовано {updated} послуг(и).')


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    """Адмін панель для PricingPlan"""

    list_display = (
        'name',
        'service_link',
        'plan_type_display',
        'price_display',
        'sessions_count',
        'discount_percent',
        'price_per_session_display',
        'is_default',
    )

    list_filter = (
        'plan_type',
        'is_default',
        'service__category',
    )

    search_fields = (
        'name',
        'service__name',
    )

    ordering = ('service', 'price')

    fieldsets = (
        ('📋 Основна інформація', {
            'fields': (
                'service',
                'name',
                'plan_type',
            )
        }),
        ('💰 Ціноутворення', {
            'fields': (
                'price',
                'sessions_count',
                'discount_percent',
                'is_default',
            )
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['service']

    @admin.display(description='Послуга')
    def service_link(self, obj):
        """Посилання на послугу"""
        url = f"/admin/elevix/service/{obj.service.pk}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.service.name
        )

    @admin.display(description='Тип')
    def plan_type_display(self, obj):
        """Відображення типу плану"""
        icons = {
            'single': '1️⃣',
            'package': '📦',
        }
        icon = icons.get(obj.plan_type, '')
        return format_html('{} {}', icon, obj.get_plan_type_display())

    @admin.display(description='Ціна')
    def price_display(self, obj):
        """Відображення ціни"""
        return format_html('<strong style="color: green;">{} грн</strong>', obj.price)

    @admin.display(description='Ціна/заняття')
    def price_per_session_display(self, obj):
        """Ціна за одне заняття"""
        price = obj.get_price_per_session()
        return format_html('<span style="color: blue;">{:.2f} грн</span>', price)


@admin.register(ServiceFeature)
class ServiceFeatureAdmin(admin.ModelAdmin):
    """Адмін панель для ServiceFeature"""

    list_display = (
        'feature_text',
        'service_link',
        'icon',
        'sort_order',
    )

    list_filter = (
        'service__category',
    )

    search_fields = (
        'feature_text',
        'service__name',
    )

    ordering = ('service', 'sort_order')

    fields = (
        'service',
        'feature_text',
        'icon',
        'sort_order',
    )

    autocomplete_fields = ['service']

    @admin.display(description='Послуга')
    def service_link(self, obj):
        """Посилання на послугу"""
        url = f"/admin/elevix/service/{obj.service.pk}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.service.name
        )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Адмін панель для Booking"""

    list_display = (
        'id',
        'user_link',
        'service_link',
        'booking_date',
        'status_display',
        'total_price_display',
        'sessions_info',
        'created_at',
    )

    list_filter = (
        'status',
        'service__category',
        'booking_date',
        'created_at',
    )

    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'service__name',
    )

    ordering = ('-booking_date',)

    fieldsets = (
        ('👤 Клієнт', {
            'fields': ('user',)
        }),
        ('📋 Послуга', {
            'fields': (
                'service',
                'pricing_plan',
            )
        }),
        ('📅 Дата та статус', {
            'fields': (
                'booking_date',
                'status',
            )
        }),
        ('💰 Фінанси', {
            'fields': (
                'total_price',
            )
        }),
        ('📊 Заняття (для пакетів)', {
            'fields': (
                'sessions_total',
                'sessions_remaining',
            ),
            'classes': ('collapse',),
        }),
        ('📝 Додаткова інформація', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ['user', 'service', 'pricing_plan']

    @admin.display(description='Користувач')
    def user_link(self, obj):
        """Посилання на користувача"""
        url = f"/admin/elevix/gymuser/{obj.user.pk}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.user.get_full_name()
        )

    @admin.display(description='Послуга')
    def service_link(self, obj):
        """Посилання на послугу"""
        url = f"/admin/elevix/service/{obj.service.pk}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.service.name
        )

    @admin.display(description='Статус')
    def status_display(self, obj):
        """Відображення статусу з кольорами"""
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'completed': 'green',
            'cancelled': 'red',
        }
        icons = {
            'pending': '⏳',
            'confirmed': '✅',
            'completed': '🎉',
            'cancelled': '❌',
        }
        color = colors.get(obj.status, 'gray')
        icon = icons.get(obj.status, '')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )

    @admin.display(description='Сума')
    def total_price_display(self, obj):
        """Відображення суми"""
        return format_html('<strong style="color: green;">{} грн</strong>', obj.total_price)

    @admin.display(description='Заняття')
    def sessions_info(self, obj):
        """Інформація про заняття"""
        if obj.sessions_total:
            return format_html(
                '<span style="color: blue;">{} / {}</span>',
                obj.sessions_remaining,
                obj.sessions_total
            )
        return '—'

    actions = ['confirm_bookings', 'complete_bookings', 'cancel_bookings']

    @admin.action(description='✅ Підтвердити обрані бронювання')
    def confirm_bookings(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'Підтверджено {updated} бронювань.')

    @admin.action(description='🎉 Завершити обрані бронювання')
    def complete_bookings(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, f'Завершено {updated} бронювань.')

    @admin.action(description='❌ Скасувати обрані бронювання')
    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'Скасовано {updated} бронювань.')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """Адмін панель для Schedule"""

    list_display = (
        'trainer_link',
        'service_link',
        'day_of_week_display',
        'time_range',
        'max_participants',
        'is_active',
    )

    list_filter = (
        'day_of_week',
        'is_active',
        'trainer__specialization',
    )

    search_fields = (
        'trainer__first_name',
        'trainer__last_name',
        'service__name',
    )

    ordering = ('day_of_week', 'start_time')

    fieldsets = (
        ('👨‍🏫 Тренер та послуга', {
            'fields': (
                'trainer',
                'service',
            )
        }),
        ('📅 Розклад', {
            'fields': (
                'day_of_week',
                ('start_time', 'end_time'),
            )
        }),
        ('👥 Учасники', {
            'fields': (
                'max_participants',
                'is_active',
            )
        }),
    )

    autocomplete_fields = ['trainer', 'service']

    @admin.display(description='Тренер')
    def trainer_link(self, obj):
        """Посилання на тренера"""
        url = f"/admin/elevix/trainer/{obj.trainer.pk}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.trainer.get_full_name()
        )

    @admin.display(description='Послуга')
    def service_link(self, obj):
        """Посилання на послугу"""
        url = f"/admin/elevix/service/{obj.service.pk}/change/"
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.service.name
        )

    @admin.display(description='День тижня')
    def day_of_week_display(self, obj):
        """Відображення дня тижня"""
        emojis = ['📅', '📅', '📅', '📅', '📅', '📅', '📅']
        emoji = emojis[obj.day_of_week]
        return format_html('{} {}', emoji, obj.get_day_of_week_display())

    @admin.display(description='Час')
    def time_range(self, obj):
        """Діапазон часу"""
        return format_html(
            '<strong>{} - {}</strong>',
            obj.start_time.strftime('%H:%M'),
            obj.end_time.strftime('%H:%M')
        )

    actions = ['activate_schedules', 'deactivate_schedules']

    @admin.action(description='✅ Активувати обрані розклади')
    def activate_schedules(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активовано {updated} розкладів.')

    @admin.action(description='❌ Деактивувати обрані розклади')
    def deactivate_schedules(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивовано {updated} розкладів.')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Адмін панель для FAQ"""

    list_display = (
        'question_preview',
        'answer_preview',
        'sort_order',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
        'created_at',
    )

    search_fields = (
        'question',
        'answer',
    )

    ordering = ('sort_order', 'id')

    fieldsets = (
        ('❓ Питання та відповідь', {
            'fields': (
                'question',
                'answer',
            )
        }),
        ('⚙️ Налаштування', {
            'fields': (
                'sort_order',
                'is_active',
            )
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Питання')
    def question_preview(self, obj):
        """Попередній перегляд питання"""
        return format_html(
            '<strong>{}</strong>',
            obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
        )

    @admin.display(description='Відповідь')
    def answer_preview(self, obj):
        """Попередній перегляд відповіді"""
        preview = obj.answer[:100] + '...' if len(obj.answer) > 100 else obj.answer
        return format_html('<span style="color: gray;">{}</span>', preview)

    actions = ['activate_faqs', 'deactivate_faqs']

    @admin.action(description='✅ Активувати обрані питання')
    def activate_faqs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активовано {updated} питань.')

    @admin.action(description='❌ Деактивувати обрані питання')
    def deactivate_faqs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивовано {updated} питань.')


# Налаштування заголовків адмін панелі
admin.site.site_header = "Elevix - Адміністрування"
admin.site.site_title = "Elevix Admin"
admin.site.index_title = "Панель керування спортзалом"

