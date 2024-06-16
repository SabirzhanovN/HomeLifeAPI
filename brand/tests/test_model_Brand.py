from django.test import TestCase
from brand.models import Brand


class BrandTestCase(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(
            name="Samsung"
        )

    def test_brand_creation(self):
        brand = Brand.objects.create(
            name="Samsung"
        )

        self.assertEqual(brand.id, self.brand.id + 1)
        self.assertEqual(brand.name, "Samsung")

    def test_brand_str_method(self):
        self.assertEqual(str(self.brand), "Samsung")

    def tearDown(self):
        self.brand.delete()
