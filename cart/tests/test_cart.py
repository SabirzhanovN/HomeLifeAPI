from django.test import TestCase, RequestFactory
from django.conf import settings
from django.utils import timezone

from brand.models import Brand
from cart.service import Cart
from discount.models import Discount
from shop.models import Product, ProductType, Category, Catalog
from decimal import Decimal


class CartTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.session = self.client.session
        self.cart = Cart(self.request)

    @staticmethod
    def create_product():
        catalog = Catalog.objects.create(name='cat x')
        category = Category.objects.create(name='Electronics', catalog=catalog)
        product_type = ProductType.objects.create(name='Electronics', category=category)
        brand = Brand.objects.create(name='Brand X')

        product = Product.objects.create(
            name='Product X',
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

    def test_cart_initialization(self):
        self.assertEqual(self.cart.cart, {})

    def test_add_product_to_cart(self):
        product = self.create_product()
        self.cart.add({"id": product.id})
        self.assertIn(str(product.id), self.cart.cart)
        self.assertEqual(self.cart.cart[str(product.id)]["quantity"], 1)

    def test_add_product_with_quantity(self):
        product = self.create_product()
        self.cart.add({"id": product.id}, quantity=3)
        self.assertEqual(self.cart.cart[str(product.id)]["quantity"], 3)

    def test_add_product_with_override_quantity(self):
        product = self.create_product()
        self.cart.add({"id": product.id}, quantity=3)
        self.cart.add({"id": product.id}, quantity=2, override_quantity=True)
        self.assertEqual(self.cart.cart[str(product.id)]["quantity"], 2)

    def test_remove_product_from_cart(self):
        product = self.create_product()
        self.cart.add({"id": product.id})
        self.cart.remove({"id": product.id})
        self.assertNotIn(str(product.id), self.cart.cart)

    def test_cart_len(self):
        product = self.create_product()
        self.cart.add({"id": product.id}, quantity=2)
        self.assertEqual(len(self.cart), 2)

    def test_get_total_price(self):
        product = self.create_product()
        self.cart.add({"id": product.id}, quantity=2)
        self.assertEqual(self.cart.get_total_price(), Decimal("20.00"))

    def test_clear_cart(self):
        product = self.create_product()
        self.cart.add({"id": product.id})
        self.cart.clear()
        self.assertTrue(self.request.session.modified)
        # self.assertEqual(self.cart.cart, {}) ???

    def test_add_invalid_product(self):
        with self.assertRaises(ValueError):
            self.cart.add({"id": 999})

    def test_add_product_without_id(self):
        with self.assertRaises(IndexError):
            self.cart.add({})

    def test_remove_invalid_product(self):
        with self.assertRaises(IndexError):
            self.cart.remove({})

    def test_iterate_cart(self):
        product = self.create_product()
        self.cart.add({"id": product.id})
        items = list(self.cart)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["quantity"], 1)
        self.assertEqual(items[0]["price"], Decimal("10.00"))

    # def test_iterate_cart_with_price_after_discount(self):
    #     product = self.create_product()
    #
    #     discount = Discount.objects.create(
    #         percent=50,
    #     )
    #     discount.products.add(product)
    #
    #     self.cart.add({"id": product.id})
    #     items = list(self.cart)
    #     self.assertEqual(len(items), 1)
    #     self.assertEqual(items[0]["quantity"], 1)
    #     print(items[0])
    #     self.assertEqual(items[0]["price"], Decimal("5.00"))

    def test_save_method(self):
        product = self.create_product()
        self.cart.add({"id": product.id})
        self.cart.save()
        self.assertTrue(self.request.session.modified)
