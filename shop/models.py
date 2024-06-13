from django.db import models
from brand.models import Brand


class Catalog(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Catalog'
        verbose_name_plural = 'Catalogs'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)
    # Html color code(or rgb)
    color_code = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Model for selecting the type of product in a specific category.
    Since, for example, the "type" fields of washing machines are
    different from refrigerators or vacuum cleaners
    """
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.category.name} - {self.name} type'


class Product(models.Model):
    name = models.CharField(max_length=255)
    grade = models.DecimalField(
        default=0,
        max_digits=2,
        decimal_places=1
    )
    color = models.ManyToManyField(
        Color,
        related_name='color'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    # If the product is included in the list of discounts, the price after the discount will change
    price_after_discount = models.DecimalField(
        default=None,
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    discount_percent = models.IntegerField(
        default=0
    )

    # Each product of a certain category can have different fields "base_characteristic", "about_product".
    # For this reason, the field data in the JSONField type
    base_characteristics = models.JSONField()
    about_product = models.JSONField()

    type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    main_image = models.ImageField(upload_to='ProductImages')
    image_1 = models.ImageField(upload_to='ProductImages', null=True, blank=True)
    image_2 = models.ImageField(upload_to='ProductImages', null=True, blank=True)

    power = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date_of_create = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
