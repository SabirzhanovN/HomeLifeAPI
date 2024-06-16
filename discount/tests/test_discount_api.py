from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Product, Catalog, Category, ProductType
from discount.models import Discount
from brand.models import Brand


user = get_user_model()


class DiscountViewSetTestCase(TestCase):
    @staticmethod
    def create_product(product_name, price):
        catalog = Catalog.objects.create(name='cat x')
        category = Category.objects.create(name='Electronics', catalog=catalog)
        product_type = ProductType.objects.create(name='Electronics', category=category)
        brand = Brand.objects.create(name='Brand X')

        product = Product.objects.create(
            name=product_name,
            grade=Decimal('4.5'),
            price=Decimal(price),
            price_after_discount=Decimal(0),
            discount_percent=0,
            base_characteristics={'weight': '1kg', 'size': 'small'},
            about_product={'description': 'Lorem ipsum dolor sit amet'},
            type=product_type,
            brand=brand,
            category=category,
            main_image='path/to/main_image.jpg',
            power='1000',
            date_of_create=timezone.now()
        )
        return product

    def setUp(self):
        self.client = APIClient()
        self.admin_user = user.objects.create_superuser(email='admin@example.com', phone="+999", password='password')
        self.client.force_authenticate(user=self.admin_user)
        self.brand = Brand.objects.create(name='Brand')
        self.product1 = self.create_product(product_name='Product 1', price=100.0)
        self.product2 = self.create_product(product_name='Product 2', price=200.0)

    def test_create_discount(self):
        data = {
            'percent': 10,
            'products': [self.product1.id, self.product2.id]
        }
        response = self.client.post('/api/discount/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Discount.objects.count(), 1)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertEqual(self.product1.price_after_discount, 90)
        self.assertEqual(self.product2.price_after_discount, 180)

    def test_update_discount(self):
        discount = Discount.objects.create(percent=10)
        discount.products.add(self.product1, self.product2)
        data = {
            'percent': 20,
            'products': [self.product2.id]
        }
        response = self.client.put(f'/api/discount/{discount.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(discount.products.count(), 1)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertEqual(self.product1.price_after_discount, None)
        self.assertEqual(self.product2.price_after_discount, 160)

    def test_delete_discount(self):
        discount = Discount.objects.create(percent=10)
        discount.products.add(self.product1, self.product2)
        response = self.client.delete(f'/api/discount/{discount.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Discount.objects.count(), 0)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()

        self.assertEqual(self.product1.price_after_discount, None)
        self.assertEqual(self.product2.price_after_discount, None)
