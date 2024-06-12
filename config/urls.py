from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # For session login
    path('account/', include('account.urls'))
]
