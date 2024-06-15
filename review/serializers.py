from decimal import Decimal

from rest_framework import serializers

from shop.models import Product
from .models import GradeDescription, Review


class GradeDescriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeDescription
        fields = ('id', 'description')
        read_only_fields = ('id', 'description')


class GradeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeDescription
        fields = ('id', 'description', 'category')
        read_only_fields = ('id',)


class ReviewSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        """
        We customize the initializer so that only the user through whom the request
        is made is displayed in the browsable api
        """
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['user'].queryset = self.fields['user'].queryset.filter(
                email=self.context['view'].request.user)

    class Meta:
        model = Review
        fields = ('id', 'product', 'content', 'user', 'grades', 'average_grade', 'date_of_create')
        read_only_fields = ('id', 'date_of_create', 'average_grade')

    def create(self, validated_data):
        """
        Override the create method so that the average rating is calculated.
        Then, so that the product rating changes when creating a review
        """
        # find average_grate for concrete review
        grades = dict(validated_data['grades'])
        grade = Decimal(sum([i for i in grades.values()]) / len(grades))

        # adding tp serializer fields, because average_grade is required field in Review model
        validated_data['average_grade'] = grade

        # find final average_grade for concrete product
        reviews = Review.objects.filter(product=validated_data['product'])
        product_average_grade = sum([i.average_grade for i in reviews] + [grade]) / (len(reviews) + 1)

        # update field grade in product
        product = Product.objects.get(id=validated_data['product'].id)
        product.grade = product_average_grade
        product.save()

        return super(ReviewSerializer, self).create(validated_data)
