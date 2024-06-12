from django.contrib import admin
from .models import Catalog, Category, ProductType, Color, Product

admin.site.register(Catalog)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Color)
admin.site.register(Product)
