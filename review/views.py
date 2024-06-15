from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from .models import GradeDescription, Review, Reply
from .serializers import GradeDescriptionSerializer, ReviewSerializer, ReplySerializer, ReviewDetailSerializer
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
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
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

    def retrieve(self, request, *args, **kwargs):
        """
        Override the retrieve method so that when the review detail is displayed,
        the responses to this review are also displayed
        """
        instance = self.get_object()
        serializer = ReviewDetailSerializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReplyViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin):
    """
    ViewSet to view the list, write a response to a review or to an answer.
    All users can post or reply to each other.
    Non-authorized users will be under the name AnonymousUser
    """
    serializer_class = ReplySerializer
    permission_classes = (AllowAny,)
    queryset = Reply.objects.all()
