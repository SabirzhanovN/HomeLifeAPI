from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('review', views.ReviewViewSet, basename='reviews')
router.register('reply', views.ReplyViewSet, basename='reply')
router.register('grade-description', views.GradeDescriptionViewSet, basename='grade-description')

urlpatterns = [
    path('', include(router.urls))
]
