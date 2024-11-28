from django.urls import path
from .views import RegistrationView, login_user, OTPVerificationAPIView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='RegistrationView'),
    path('verify-otp/', OTPVerificationAPIView.as_view(), name='OTPVerificationAPIView'),
    path('login/', login_user, name='login_user'),

]
