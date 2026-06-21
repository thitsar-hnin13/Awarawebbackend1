# social/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Post, Comment, Share
from .serializers import ProfileSerializer, PostSerializer, CommentSerializer, UserSerializer

# ========== PROFILE VIEWS ==========
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = request.user.profile
    if request.method == 'GET':
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = user.profile
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, username):
    try:
        user_to_follow = User.objects.get(username=username)
        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = user_to_follow.profile
        if request.user in profile.followers.all():
            profile.followers.remove(request.user)
            return Response({'message': f'Unfollowed {username}', 'following': False})
        else:
            profile.followers.add(request.user)
            return Response({'message': f'Followed {username}', 'following': True})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# ========== POST VIEWS ==========
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == 'GET':
        user = request.user
        admin_users = User.objects.filter(is_staff=True)
        posts = Post.objects.filter(
            Q(user=user) | Q(user__in=admin_users)
        ).distinct().order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("📝 Creating new post for user:", request.user.username)
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            print(f"✅ Post created: {post.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"❌ Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def public_posts(request):
    """Public posts - only admin/staff posts"""
    print("📢 Fetching public posts...")
    staff_users = User.objects.filter(is_staff=True)
    posts = Post.objects.filter(user__in=staff_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    print(f"📢 Found {posts.count()} public posts")
    return Response(serializer.data)

# ========== SINGLE POST VIEW (GET, PUT, DELETE) ==========
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if request.user != post.user and not request.user.is_staff:
            return Response({'error': 'You cannot view this post'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if post.user != request.user:
            return Response({'error': 'You cannot edit this post'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)

# ========== LIKE VIEW ==========
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != post.user and not request.user.is_staff:
        if not post.user.is_staff:
            return Response({'error': 'You cannot like this post'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return Response({
            'message': 'Unliked', 
            'like_count': post.likes.count(),
            'is_liked': False
        })
    else:
        post.likes.add(request.user)
        return Response({
            'message': 'Liked', 
            'like_count': post.likes.count(),
            'is_liked': True
        })

# ========== COMMENT VIEWS ==========
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def post_comments(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user != post.user and not request.user.is_staff and not post.user.is_staff:
        return Response({'error': 'You cannot view comments on this post'}, status=status.HTTP_403_FORBIDDEN)
    
    comments = post.comments.all().order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# ========== ADD COMMENT - Fixed Version ==========
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, pk):
    """Add a comment to a post"""
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    print("🔍 Comment - Request data:", request.data)
    
    # Get content from request
    content = request.data.get('content', '')
    
    if not content:
        print("❌ No content found")
        return Response(
            {'error': 'Content is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create comment directly
    comment = Comment.objects.create(
        user=request.user,
        post=post,
        content=content
    )
    
    print(f"✅ Comment created by {request.user.username}: {content[:50]}")
    
    return Response({
        'id': comment.id,
        'content': comment.content,
        'username': request.user.username,
        'created_at': comment.created_at.isoformat()
    }, status=status.HTTP_201_CREATED)

# ========== ADMIN VERIFICATION ==========
@api_view(['POST'])
@permission_classes([AllowAny])
def verify_admin(request):
    """Verify if the provided password is the admin password"""
    print("🔐 Verify admin endpoint called")
    print("Request data:", request.data)
    
    password = request.data.get('password', '')
    
    if not password:
        print("❌ No password provided")
        return Response(
            {'is_admin': False, 'error': 'Password required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    admin_users = User.objects.filter(is_staff=True)
    
    if not admin_users.exists():
        print("❌ No admin user found")
        return Response(
            {'is_admin': False, 'error': 'No admin user found'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    for admin_user in admin_users:
        if admin_user.check_password(password):
            print(f"✅ Admin verified: {admin_user.username}")
            return Response({'is_admin': True, 'message': 'Admin verified'})
    
    print("❌ Invalid admin password")
    return Response(
        {'is_admin': False, 'error': 'Invalid password'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )
# social/views.py - posts function

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == 'GET':
        user = request.user
        admin_users = User.objects.filter(is_staff=True)
        posts = Post.objects.filter(
            Q(user=user) | Q(user__in=admin_users)
        ).distinct().order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("=" * 50)
        print("📝 Creating new post for user:", request.user.username)
        print("Request data:", request.data)
        
        # Get data from request
        content = request.data.get('content', '')
        fake_view_count = request.data.get('fake_view_count', 0)
        fake_like_count = request.data.get('fake_like_count', 0)
        
        # Convert to int
        try:
            fake_view_count = int(fake_view_count)
        except:
            fake_view_count = 0
        try:
            fake_like_count = int(fake_like_count)
        except:
            fake_like_count = 0
        
        # Create post with fake counts
        post = Post.objects.create(
            user=request.user,
            content=content,
            fake_view_count=fake_view_count,
            fake_like_count=fake_like_count
        )
        
        # Handle image
        if request.data.get('image'):
            post.image = request.data.get('image')
            post.save()
        
        serializer = PostSerializer(post, context={'request': request})
        print(f"✅ Post created: {post.id}")
        print(f"   Views: {fake_view_count}, Likes: {fake_like_count}")
        print("=" * 50)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
# social/views.py (အောက်ဆုံးမှာ ထည့်ပါ)
# social/views.py# social/views.py (အောက်ဆုံးမှာ ထည့်ပါ)

from .models import Notification
from .serializers import NotificationSerializer

# ========== NOTIFICATION VIEWS ==========
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    """Get user's notifications"""
    notifications = request.user.notifications.all()
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, pk):
    """Mark a single notification as read"""
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return Response({'message': 'Marked as read', 'success': True})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    count = request.user.notifications.filter(is_read=False).update(is_read=True)
    return Response({'message': f'{count} notifications marked as read', 'success': True})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, pk):
    """Delete a notification"""
    try:
        notification = Notification.objects.get(pk=pk, user=request.user)
        notification.delete()
        return Response({'message': 'Notification deleted', 'success': True})
    except Notification.DoesNotExist:
        return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)
# social/views.py

@api_view(['GET'])
@permission_classes([AllowAny])
def public_posts(request):
    """Public posts - everyone can see all posts"""
    print("📢 Fetching public posts...")
    # Show ALL posts to everyone (not just admin)
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    print(f"📢 Found {posts.count()} public posts")
    return Response(serializer.data)