# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from .utils import send_welcome_email
from django.db.models import Count
from projects.models import Project
from blog.models import BlogPost
from contacts.models import ContactMessage
# ========== AUTH VIEWS ==========
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not user.check_password(current_password):
        return Response({'error': 'Current password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    
    if len(new_password) < 6:
        return Response({'error': 'Password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
# accounts/views.py

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,  # user data ပြန်ပို့မယ်
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    if request.user.is_authenticated:
        # Get or create profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        return Response(UserSerializer(request.user).data)
    return Response({'error': 'Not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

# ========== PROFILE VIEWS ==========

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        from .serializers import ProfileSerializer
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        from .serializers import ProfileSerializer
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_avatar(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if 'avatar' in request.FILES:
        profile.avatar = request.FILES['avatar']
        profile.save()
        # Return full URL
        avatar_url = request.build_absolute_uri(profile.avatar.url)
        return Response({'message': 'Avatar uploaded', 'url': avatar_url})
    return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_cover(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if 'cover_image' in request.FILES:
        profile.cover_image = request.FILES['cover_image']
        profile.save()
        cover_url = request.build_absolute_uri(profile.cover_image.url)
        return Response({'message': 'Cover uploaded', 'url': cover_url})
    return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # ✅ Send welcome email
        send_welcome_email(user)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registration successful',
            'user': UserSerializer(user).data,
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Get dashboard statistics for the current user"""
    user = request.user
    
    # Get user's projects
    projects = Project.objects.all().order_by('-created_at')[:5]
    
    # Get user's blog posts
    blog_posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:5]
    
    # Get contact messages
    messages = ContactMessage.objects.all().order_by('-created_at')[:5]
    
    # Calculate stats
    total_projects = Project.objects.count()
    total_blogs = BlogPost.objects.filter(is_published=True).count()
    total_messages = ContactMessage.objects.count()
    total_views = 15200  # You can implement real view tracking
    
    # Recent activities
    recent_activities = []
    
    for project in projects[:3]:
        recent_activities.append({
            'user': user.username,
            'action': f'created project "{project.title}"',
            'time': project.created_at.strftime('%Y-%m-%d %H:%M'),
            'type': 'project'
        })
    
    for post in blog_posts[:3]:
        recent_activities.append({
            'user': user.username,
            'action': f'published blog "{post.title}"',
            'time': post.created_at.strftime('%Y-%m-%d %H:%M'),
            'type': 'blog'
        })
    
    # Recent projects for table
    recent_projects_data = []
    for project in projects:
        recent_projects_data.append({
            'id': project.id,
            'name': project.title,
            'status': 'In Progress',
            'progress': 75,
            'deadline': project.created_at.strftime('%b %d, %Y'),
            'priority': 'High' if project.category == 'Web' else 'Medium'
        })
    
    # Top performing posts
    top_posts_data = []
    for post in blog_posts[:3]:
        top_posts_data.append({
            'id': post.id,
            'title': post.title,
            'views': '1.2k',
            'likes': 67,
            'shares': 19,
            'date': post.created_at.strftime('%b %d, %Y')
        })
    
    return Response({
        'stats': {
            'total_projects': total_projects,
            'total_blogs': total_blogs,
            'total_messages': total_messages,
            'total_views': total_views,
        },
        'recent_projects': recent_projects_data,
        'recent_activities': recent_activities,
        'top_posts': top_posts_data,
    })