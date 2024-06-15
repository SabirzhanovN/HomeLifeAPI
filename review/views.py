from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import viewsets, mixins

from .models import GradeDescription
from .serializers import GradeDescriptionSerializer


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
