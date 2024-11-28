from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('accounts.urls')),
    path("", include("seller.urls")),
    path("customer/", include("customer.urls")),
] + debug_toolbar_urls()
