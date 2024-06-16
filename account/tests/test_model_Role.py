from django.test import TestCase
from account.models import Role


class RoleModelTestCase(TestCase):
    def setUp(self):
        self.role_data = {
            "name": "Wholesaler"
        }
        self.role = Role.objects.create(**self.role_data)

    def test_role_creation(self):
        role = Role.objects.create(name="Regular")
        self.assertEqual(role.name, "Regular")

    def test_role_str_method(self):
        self.assertEqual(str(self.role), "Role Wholesaler")

    def tearDown(self):
        self.role.delete()
