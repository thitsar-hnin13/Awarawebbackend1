# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar_url = serializers.SerializerMethodField()
    cover_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        if obj.avatar:
            return obj.avatar.url
        return None
    
    def get_cover_url(self, obj):
        if obj.cover_image:
            return obj.cover_image.url
        return None

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "No user found with this email"})

        if not user:
            raise serializers.ValidationError({"error": "Invalid password"})

        refresh = RefreshToken.for_user(user)
        
        return {
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'message': 'Login successful'
        }

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match"})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists"})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists"})
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user