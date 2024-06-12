from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('catalog', views.CatalogViewSet, basename='catalog')
router.register('category', views.CategoryViewSet, basename='category')
router.register('product-type', views.ProductTypeViewSet, basename='product-type')
router.register('color', views.ColorViewSet, basename='color')

urlpatterns = [
    path('', include(router.urls))
]
