from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),

    # Register new User(Client)/ change fields(password, email, phone...)
    re_path(r'^auth/', include('djoser.urls')),
    # Login/logout with token
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    # For session login/logout
    path('api/account/', include('account.urls')),

    # API
    path('api/shop/', include('shop.urls')),
    path('api/brand/', include('brand.urls')),
    path('api/discount/', include('discount.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/review/', include('review.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
