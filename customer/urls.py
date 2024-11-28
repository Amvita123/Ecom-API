from django.urls import path
from .views import CustomerProfileView, OrderView

urlpatterns = [
    path('products/', CustomerProfileView.as_view(), name='CustomerProfileView'),
    path('orders/', OrderView.as_view(), name='customer-order-list'),
]
