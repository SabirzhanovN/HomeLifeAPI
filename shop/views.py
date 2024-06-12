from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import (CatalogSerializer, CategorySerializer, ProductTypeSerializer,
                          ColorSerializer, ProductSerializer, ProductListSerializer)
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


class ProductListRetrieveViewSet(viewsets.GenericViewSet,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    """
    ViewSet for Listing and Detail(Retrieve) Product objects. Authorized and non-authorized users have access
    """
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        """
        Customization retrieve for detail Product
        Because the default serializer does not provide complete information about the product
        """
        instance = self.get_object()
        serializer = ProductSerializer(instance)
        return Response(serializer.data)


class ProductCreateUpdateDestroyViewSet(viewsets.GenericViewSet,
                                        mixins.CreateModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin):
    """
    ViewSet for admin User only to create, update, and delete a Product object.
    Standard users and anonymous users do not have access
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    queryset = Product.objects.all()

