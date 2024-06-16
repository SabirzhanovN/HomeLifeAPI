from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from brand.models import Brand
from discount.models import Discount, Product
from shop.models import Catalog, Category, ProductType


class DiscountModelTestCase(TestCase):
    @staticmethod
    def create_product(product_name):
        catalog = Catalog.objects.create(name='cat x')
        category = Category.objects.create(name='Electronics', catalog=catalog)
        product_type = ProductType.objects.create(name='Electronics', category=category)
        brand = Brand.objects.create(name='Brand X')

        product = Product.objects.create(
            name=product_name,
            grade=Decimal('4.5'),
            price=Decimal('10.00'),
            price_after_discount=Decimal('0'),
            discount_percent=0,
            base_characteristics={'weight': '1kg', 'size': 'small'},
            about_product={'description': 'Lorem ipsum dolor sit amet'},
            type=product_type,
            brand=brand,
            category=category,
            main_image='path/to/main_image.jpg',
            power=Decimal('100.0'),
            date_of_create=timezone.now()
        )
        return product

    def setUp(self):
        self.product1 = self.create_product("Product 1")
        self.product2 = self.create_product("Product 2")

        self.discount = Discount.objects.create(percent=10)
        self.discount.products.add(self.product1, self.product2)

    def test_discount_creation(self):
        self.assertEqual(self.discount.percent, 10)
        self.assertIn(self.product1, self.discount.products.all())
        self.assertIn(self.product2, self.discount.products.all())

    def test_discount_str_method(self):
        self.assertEqual(str(self.discount), f"{self.discount.percent}% - {self.discount.products.__sizeof__()}")

    def tearDown(self):
        self.product1.delete()
        self.product2.delete()
        self.discount.delete()
