from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.contrib.auth.models import Group, Permission


GymUser = get_user_model()


class GymUserModelTests(TestCase):

    def test_create_user(self):
        """Тест: создание обычного пользователя"""
        user = GymUser.objects.create_user(
            email="test@example.com",
            password="12345678",
            full_name="Test User",
            phone="+380671234567"
        )
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password("12345678"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест: создание суперпользователя"""
        admin = GymUser.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            full_name="Admin"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_user_with_groups_table_missing(self):
        """Тест: имитация ситуации, когда auth_group пустая"""
        # Удаляем все группы
        Group.objects.all().delete()

        # Создаем пользователя, чтобы проверить — не падает ли IntegrityError
        try:
            user = GymUser.objects.create_user(
                email="broken@example.com",
                password="broken123",
                full_name="Broken User",
            )
            user.groups.clear()  # безопасность
            user.user_permissions.clear()
            user.save()
        except IntegrityError as e:
            self.fail(f"IntegrityError возник: {e}")

        self.assertTrue(GymUser.objects.filter(email="broken@example.com").exists())

    def test_create_user_with_default_group(self):
        """Тест: если группа Default существует — пользователь добавляется в неё"""
        group, _ = Group.objects.get_or_create(name="Default")

        user = GymUser.objects.create_user(
            email="default@example.com",
            password="default123",
            full_name="Default User"
        )
        user.groups.add(group)
        user.save()

        self.assertIn(group, user.groups.all())
