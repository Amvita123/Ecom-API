from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductProfileView.as_view(), name='ProductProfileView'),
    path('products/<int:pk>/', ProductProfileView.as_view(), name='product-detail'),
    path('orders/', OrderView.as_view(), name='Order-View'),
    path('orders/<int:order_id>/', OrderView.as_view(), name='order-update'),
]

