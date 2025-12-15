from django.core.management.base import BaseCommand
from elevix.models import Service, PricingPlan, ServiceFeature


class Command(BaseCommand):
    help = 'Завантажити послуги з карток'

    def handle(self, *args, **options):
        # Очистити старі дані (опціонально)
        ServiceFeature.objects.all().delete()
        PricingPlan.objects.all().delete()
        Service.objects.all().delete()

        # ММА
        mma = Service.objects.create(
            name="Групове тренування з ММА, будні дні",
            description="Тренування з змішаних бойових мистецтв у групі",
            duration=1.20,
            category="group_training",
            is_active=True
        )

        PricingPlan.objects.create(
            service=mma, name="Разове", plan_type="single",
            price=900, is_default=True
        )

        PricingPlan.objects.create(
            service=mma, name="Пакет з 10 занять", plan_type="package",
            price=8000, sessions_count=10, discount_percent=11.11
        )

        ServiceFeature.objects.create(
            service=mma,
            feature_text="Маєте перевагу у тренуванні",
            sort_order=1
        )

        ServiceFeature.objects.create(
            service=mma,
            feature_text="Зможете індивідуально відпрацювати все що потрібно",
            sort_order=2
        )

        ServiceFeature.objects.create(
            service=mma,
            feature_text="Обрати групу можна взалежнос і від віку та навичок",
            sort_order=3
        )

        # Бокс
        boxing = Service.objects.create(
            name="Персональне тренування з бокс",
            description="Індивідуальні тренування з боксу",
            duration=1.00,
            category="personal_training",
            is_active=True
        )

        PricingPlan.objects.create(
            service=boxing, name="Разове", plan_type="single",
            price=950, is_default=True
        )

        PricingPlan.objects.create(
            service=boxing, name="Пакет з 10 занять", plan_type="package",
            price=8500, sessions_count=10
        )

        ServiceFeature.objects.create(
            service=boxing,
            feature_text="Маєте перевагу у тренуванні",
            sort_order=1
        )

        ServiceFeature.objects.create(
            service=boxing,
            feature_text="Зможете індивідуально відпрацювати все що потрібно",
            sort_order=2
        )

        # Масаж
        massage = Service.objects.create(
            name="Розслаблюючі масажі",
            description="Професійний розслаблюючий масаж",
            duration=1.50,
            category="massage",
            is_active=True
        )

        PricingPlan.objects.create(
            service=massage, name="Разове", plan_type="single",
            price=750, is_default=True
        )

        PricingPlan.objects.create(
            service=massage, name="Пакет з 9 сеансів", plan_type="package",
            price=7250, sessions_count=9
        )

        ServiceFeature.objects.create(
            service=massage,
            feature_text="Розслаблені чани",
            sort_order=1
        )

        ServiceFeature.objects.create(
            service=massage,
            feature_text="Відновлювальні масажі",
            sort_order=2
        )

        self.stdout.write(
            self.style.SUCCESS('✅ Успішно завантажено всі послуги!')
        )