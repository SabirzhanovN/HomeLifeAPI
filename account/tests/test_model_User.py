from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Role

User = get_user_model()


class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.role_male = Role.objects.create(name='Male')
        cls.role_female = Role.objects.create(name='Female')

    def setUp(self):
        self.user_data = {
            "first_name": "John",
            "age": 30,
            "gender": 1,
            "role": self.role_male,
            "email": "john@example.com",
            "phone": "1234567890",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
        }

    def test_create_user(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.age, 30)
        self.assertEqual(user.gender, 1)
        self.assertEqual(user.role, self.role_male)
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.phone, "1234567890")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.date_joined)
        self.assertIsNone(user.last_login)

    def test_create_superuser(self):
        admin_data = self.user_data.copy()
        admin_data.update({
            "is_staff": True,
            "is_superuser": True
        })
        admin = User.objects.create_superuser(**admin_data)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_str_method(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), "john@example.com")

    def tearDown(self):
        User.objects.all().delete()
        Role.objects.all().delete()
