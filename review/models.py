from django.contrib.auth import get_user_model
from django.db import models

from shop.models import Category, Product

user = get_user_model()


class GradeDescription(models.Model):
    """
    Each product of a certain category may have different rating fields.
    For example, in a Washing Machine - the quality of washing, the quality of spinning.
    And the refrigerator has a noise rating and cooling quality.
    """
    description = models.CharField(max_length=255)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='grade_descriptions'
    )

    def __str__(self):
        return f"{str(self.category)} - {self.description}"


class Review(models.Model):
    content = models.TextField()

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        null=True, blank=True,
        default=None
    )

    grades = models.JSONField()
    average_grade = models.DecimalField(
        decimal_places=2,
        max_digits=3
    )
    date_of_create = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        The user field is None by default, and if the review is written by an authorized client, the field will change.
        If a review is written by someone who is not authorized, then the user field in the review
        will become AnonymousUser.


        * It turns out that any interested clients can leave reviews and ratings
        """
        if not self.user:
            # We take the previously created AnonymousUser from the database.
            # If it doesn't exist, we create it
            self.user, created = user.objects.get_or_create(
                email="Anonymous@Anonymous",
                defaults={
                    "first_name": "AnonymousUser",
                    "email": "Anonymous@Anonymous",
                    "phone": "0",
                    "password": "anonymous_user"
                }
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{str(self.user.email)} - {self.product.name} - {self.content[:20]}"


class Reply(models.Model):
    user = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        null=True, blank=True,
        default=None
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    content = models.TextField()
    date_of_create = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

    def save(self, *args, **kwargs):
        if not self.user:
            # We take the previously created AnonymousUser from the database.
            # If it doesn't exist, we create it
            self.user, created = user.objects.get_or_create(
                email="Anonymous@Anonymous",
                defaults={
                    "first_name": "AnonymousUser",
                    "email": "Anonymous@Anonymous",
                    "phone": "0",
                    "password": "anonymous_user"
                }
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reply to reply with id={str(self.parent.id)}" if self.parent \
          else f"Reply to review with id={str(self.review.id)}"
