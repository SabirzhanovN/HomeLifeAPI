from django.db import models
from shop.models import Product


class Discount(models.Model):
    percent = models.IntegerField()

    products = models.ManyToManyField(
        Product,
    )

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'

    def __str__(self):
        return f'{str(self.percent)}% - {str(self.products)}'
