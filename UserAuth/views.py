from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationsSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from .models import User
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import os


# Create your views here.

# Generate Token Manually
def get_tokens_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }
    
# User Profile
class UserRegistrationView(APIView):
    def post(self,request,format=None): 
        email = request.data['email']
        role = request.data['role']
        print("role", role)
        user_instance = User.objects.filter(email=email)
        if user_instance:
            return Response({'error':'User with given email already exists'})
        else:
            serializer = UserRegistrationsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                return Response({'massage':'Registration Successfull'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        
        print(user)
        if user is not None:
            role = user.role
            print(user.role)
            token = get_tokens_for_user(user)
            return Response({'token':token, 'role':role,'massage':'Login SuccessFully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or password is not valid']}},status=status.HTTP_404_NOT_FOUND) 
               
class UserLogoutView(APIView):
    def post(self,request):
        token = request.headers.get('Authorization')
        if token:
            logout(request)
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        serializer= UserProfileSerializer(request.user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'massage':'Change password SuccessFully'}, status=status.HTTP_200_OK)
    
class SendPasswordResetEmailView(APIView):
    permission_classes = [AllowAny]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): 
            return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
