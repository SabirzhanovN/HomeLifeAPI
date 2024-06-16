from django.test import TestCase
from payment.models import Order


class OrderModelTestCase(TestCase):
    def setUp(self):
        self.order_data = {
            "products": ["Product 1", "Product 2"],
            "first_name": "John",
            "last_name": "Doe",
            "contact": "john.doe@example.com",
            "address": "123 Main St",
            "address_additional": "Apt 1",
            "total_price": 100.50,
            "payment_type": 1,
            "status": False
        }
        self.order = Order.objects.create(**self.order_data)

    def test_order_creation(self):
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.products, self.order_data["products"])
        self.assertEqual(order.first_name, self.order_data["first_name"])
        self.assertEqual(order.last_name, self.order_data["last_name"])
        self.assertEqual(order.contact, self.order_data["contact"])
        self.assertEqual(order.address, self.order_data["address"])
        self.assertEqual(order.address_additional, self.order_data["address_additional"])
        self.assertEqual(order.total_price, self.order_data["total_price"])
        self.assertEqual(order.payment_type, self.order_data["payment_type"])
        self.assertEqual(order.status, self.order_data["status"])

    def test_order_str_method(self):
        self.assertEqual(str(self.order), f"{str(self.order.id)} of {self.order.get_full_name()}")

    def test_order_get_full_name_method(self):
        self.assertEqual(self.order.get_full_name(), "John Doe")

