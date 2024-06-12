from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import mixins

from .serializers import (CatalogSerializer, CategorySerializer, ProductTypeSerializer,
                          ColorSerializer, ProductSerializer)
from .permissions import IsAdminOrReadOnly
from .models import Catalog, Category, ProductType, Color, Product


class CatalogViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    """
    ViewSet for listing, creating, deleting, updating Catalog objects.
    - List Catalog objects can be done by all anonymous and authorized users
    - Create, Update, Delete requests can only be made by admin users

    *Update, Delete requests only via pk.
    """
    serializer_class = CatalogSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Catalog.objects.all()


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    """
    ViewSet for listing, creating, deleting, updating Category objects.
    - List Category objects can be done by all anonymous and authorized users
    - Create, Update, Delete requests can only be made by admin users

    *Update, Delete requests only via pk.
    """
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Category.objects.all()


class ProductTypeViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    """
    ViewSet for listing, creating, deleting, updating ProductType objects.
    - List ProductType objects can be done by all anonymous and authorized users
    - Create, Update, Delete requests can only be made by admin users

    *Update, Delete requests only via pk.
    """

    serializer_class = ProductTypeSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminOrReadOnly,)
    queryset = ProductType.objects.all()


class ColorViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    """
    ViewSet for listing, creating, deleting, updating Color objects.
    - List Color objects can be done by all anonymous and authorized users
    - Create, Update, Delete requests can only be made by admin users

    *Update, Delete requests only via pk.
    """

    serializer_class = ColorSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Color.objects.all()
