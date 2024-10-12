from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
import os

# User Profile
class UserRegistrationsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            return serializers.ValidationError('Password does not match')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            role = validated_data['role'],
            password = validated_data['password']
            )
        return user

        
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email','password']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','mobile_number']
        
class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'pasword2'})
    
    class Meta:
        fields = ['password','password2']
        
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm Password does not match')
        user.set_password(password)
        user.save()
        return attrs
    
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send EMail
            body = 'Click Following Link to Reset Your Password '+link
            data = {
            'subject':'Reset Your Password',
            'body':body,
            'to_email':user.email}
            print (os.environ.get("EMAIL_USER"))           
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')    
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password2'}, write_only=True)
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            print(id)
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            print(user.password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
        
# class UserPasswordResetSerializer(serializers.Serializer):
#     password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
#     password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

#     class Meta:
#         fields = ['password', 'password2']

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password2 = attrs.get('password2')
#         uid = self.context.get('uid')
#         token = self.context.get('token')

#         if password != password2:
#             raise serializers.ValidationError("Password and Confirm Password don't match")

#         try:
#             # Ensure UID decoding succeeds
#             id = smart_str(urlsafe_base64_decode(uid))
#             user = User.objects.get(id=id)
#         except (DjangoUnicodeDecodeError, User.DoesNotExist) as e:
#             raise serializers.ValidationError('Invalid UID')

#         # Validate token
#         if not PasswordResetTokenGenerator().check_token(user, token):
#             raise serializers.ValidationError('Token is not Valid or Expired')

#         # Set and save the new password
#         user.set_password(password)
#         user.save()

#         return attrs
