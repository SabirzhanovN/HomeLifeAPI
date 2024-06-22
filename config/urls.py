from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="HomeLife API",
        default_version="version 1.0",
        description="Swagger (documentation) for HomeLifeAPI project",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Register new User(Client)/ change fields(password, email, phone...)
    re_path(r'^auth/', include('djoser.urls')),
    # Login/logout with token
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # For session login/logout
    path('api/account/', include('account.urls')),

    # API
    path('api/shop/', include('shop.urls')),
    path('api/brand/', include('brand.urls')),
    path('api/discount/', include('discount.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/review/', include('review.urls')),
    path('api/payment/', include('payment.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
