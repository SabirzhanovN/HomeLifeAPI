from django.db import models

from shop.models import Category


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
