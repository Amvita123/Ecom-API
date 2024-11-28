from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import RegisterSerializers, userSerializer, OTPVerificationSerializer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
import random
from .services import send_welcome_mail, send_otp_mail


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = random.randint(100000, 999999)
            user = serializer.save(is_active=False)
            if user.is_seller:
                send_welcome_mail(user.email, user.username)
            else:
                user.otp = otp
                user.save()
                send_otp_mail(user.email, user.otp)
            user_data = serializer.data
            return Response({"detail": "User Registration Successful", "user": user_data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        serislizer = LoginSerializer(data=request.data)
        if serislizer.is_valid(raise_exception=True):
            user = serislizer.validated_data['user']
            password = serislizer.validated_data['password']
            user = authenticate(username=user.username, password=password)
            if user is None:
                return Response({"message": "Invalid Password"}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            user_data_serializer = userSerializer(user)
            return Response({
                'message': 'User login Successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "data": user_data_serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serislizer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerificationAPIView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.validated_data['otp']
            user_id = serializer.validated_data['user_id']
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            if otp == str(user.otp):
                user.is_active = True
                user.save()
                return Response({"message": "OTP verified, Please login"})
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


