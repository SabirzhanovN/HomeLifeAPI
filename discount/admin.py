from django.contrib import admin

from shop.models import Product
from .models import Discount


class DiscountAdmin(admin.ModelAdmin):
    """
    Custom ModelAdmin class for creating, modifying, and deleting discounts.
    """
    def save_model(self, request, obj, form, change):
        """
        Creating a discount. All products specified when creating a discount will update
        their price_after_discount, discount_percent fields
        """
        super().save_model(request, obj, form, change)

        for product in obj.products.all():
            product.price_after_discount = product.price - (product.price * obj.percent / 100)
            product.discount_percent = obj.percent
            product.save()

    def save_related(self, request, form, formsets, change):
        """
        Update discount. All updates will update the price_after_discount fields discount_percent in the products
        """
        if change:
            old_products = set(form.initial['products'])
            new_products = set(form.cleaned_data['products'])

            for product in old_products:
                product.price_after_discount = None
                product.discount_percent = 0
                product.save()
                print(f"Remove discount from {product.name}. price_after_discount -> {product.price_after_discount}")

            for product in new_products:
                product.price_after_discount = product.price - (product.price * form.instance.percent / 100)
                product.discount_percent = form.instance.percent
                product.save()
                print(f"Add discount to {product.name}. price_after_discount changed to {product.price_after_discount}")

            discount = Discount.objects.get(pk=form.instance.id)
            for p in old_products:
                discount.products.remove(p)

            for p in new_products:
                discount.products.add(p)

            discount.save()
            return

        super().save_related(request, form, formsets, change)

        for product in form.instance.products.all():
            product.price_after_discount = product.price - (product.price * form.instance.percent / 100)
            product.discount_percent = form.instance.percent
            product.save()
            print(f"Add discount to {product.name}. price_after_discount changed to {product.price_after_discount}")

    def delete_model(self, request, obj):
        """
        Delete a single discount object.
        - price_after_discount -> null
        - discount_percent -> 0
        """
        for product in obj.products.all():
            product.price_after_discount = None
            product.discount_percent = 0.0
            product.save()

            print(f"Remove discount from {product.name}. price_after_discount -> {product.price_after_discount}")
        obj.delete()

    def delete_queryset(self, request, queryset):
        """Selective deletion"""
        for obj in queryset:
            for product in obj.products.all():
                product.price_after_discount = None
                product.discount_percent = 0.0
                product.save()

                print(f"Remove discount from {product.name}. price_after_discount -> {product.price_after_discount}")
            obj.delete()


admin.site.register(Discount, DiscountAdmin)
