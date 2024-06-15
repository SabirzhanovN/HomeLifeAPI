from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import viewsets, mixins

from .models import GradeDescription, Review
from .serializers import GradeDescriptionSerializer, ReviewSerializer
from .filters import ReviewFilter


class GradeDescriptionViewSet(viewsets.GenericViewSet,
                              mixins.CreateModelMixin,
                              mixins.UpdateModelMixin,
                              mixins.DestroyModelMixin):
    """
    ViewSet is created for admin users. To create, update, delete GradeDescription objects
    """
    serializer_class = GradeDescriptionSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = GradeDescription.objects.all()


class ReviewViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """
    ViewSet can only create or display a review sheet.
    To receive reviews related only to a specific product, you should filter by product.

    * Example of URL
    /api/review/?product=7
    """
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)
    queryset = Review.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ReviewFilter
