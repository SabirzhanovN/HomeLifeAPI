from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import mixins

from .serializers import CatalogSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly
from .models import Catalog, Category


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
