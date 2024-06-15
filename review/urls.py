from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('', views.ReviewViewSet, basename='reviews')
router.register('grade-description', views.GradeDescriptionViewSet, basename='grade-description')

urlpatterns = [
    path('', include(router.urls))
]
