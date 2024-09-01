from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("invoices.urls")),
    path("admin/", admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),
]
