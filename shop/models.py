from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Catalog'
        verbose_name_plural = 'Catalogs'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        return self.name
