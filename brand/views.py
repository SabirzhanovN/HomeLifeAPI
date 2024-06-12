from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import mixins
from rest_framework import viewsets

from .permissions import IsAdminOrReadOnly
from .serializers import BrandSerializer
from .models import Brand


class BrandViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin):
    """
    ViewSet for listing, creating, deleting, updating brand object.
    - List brand objects can be done by all anonymous and authorized users
    - Create, Update, Delete requests can only be made by admin users
    """
    serializer_class = BrandSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    queryset = Brand.objects.all()
