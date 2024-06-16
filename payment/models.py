from django.db import models


class Order(models.Model):
    products = models.JSONField()

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True)

    contact = models.CharField(max_length=255)

    address = models.CharField(max_length=255)
    address_additional = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now=True)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    PAYMENT_TYPES = (
        (1, "By card"),
        (2, "By cash")
    )
    payment_type = models.IntegerField(choices=PAYMENT_TYPES)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"{str(self.id)} of {self.get_full_name()}"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}" if {self.last_name} else f"{self.first_name}"
        return full_name