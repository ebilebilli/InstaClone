from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Response, status
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.core.cache import cache

from apis.permission_control import AllowAny, TokenAuthentication, IsOwner, Token
from profiles.models import CustomerUser
from profiles.serializers import CustomerUserRegisterDataSerializer, LoginSerializer
from utils.otp_func import send_otp_func


class RegisterAPIView(APIView):
    """APIView for user registration."""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new user."""
        serializer = CustomerUserRegisterDataSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            send_otp_func(email) 

            otp_from_request = request.data.get('otp')
            otp_in_cache = cache.get(f'otp_{email}')

            if otp_from_request != otp_in_cache:  
                return Response({'message': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Profile created successfully',
                'username': user.username,
                'email': user.email,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(APIView):
    """
    User login API.

    POST: Accepts credentials and returns a token on success.
    """
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """
    User logout API.

    POST: Logs out the user by deleting the token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def post(self, request):
        token = request.auth
        if token:
            token.delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'No active account found'}, status=status.HTTP_400_BAD_REQUEST)