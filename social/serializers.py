# social/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Share, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    follower_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'bio', 'avatar', 'avatar_url',
                  'cover_image', 'location', 'website', 'phone', 'company', 'position',
                  'follower_count', 'following_count', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        """Get full avatar URL"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return f"/media/{obj.avatar}"
        return None


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'username', 'content', 'created_at']
        read_only_fields = ['user', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user = UserSerializer(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    view_count = serializers.IntegerField(read_only=True)
    is_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'content', 'image', 'user', 'username', 'is_staff',
                  'created_at', 'updated_at', 'like_count', 'comment_count', 
                  'is_liked', 'view_count', 'fake_view_count', 'fake_like_count']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'sender', 'sender_name', 'notification_type', 
                  'title', 'message', 'post_id', 'is_read', 'created_at']
        read_only_fields = ['user', 'created_at']
# social/serializers.py

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    follower_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    avatar_url = serializers.SerializerMethodField()  # Add this
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'username', 'email', 'bio', 'avatar', 'avatar_url',
                  'cover_image', 'location', 'website', 'phone', 'company', 'position',
                  'follower_count', 'following_count', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_avatar_url(self, obj):
        """Get full avatar URL"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return f"/media/{obj.avatar}"
        return None