from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import mixins, viewsets

from .models import Order
from .serializers import OrderSerializer
from .permissions import IsAdminUserOrCreateOnly


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    """
    A ViewSet for creating and deleting orders.

    - Allows any user to create an order.
    - Restricts order deletion to admin users only.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAdminUserOrCreateOnly,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

