# blog/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BlogPost, BlogCategory
from .serializers import BlogPostSerializer, BlogCategorySerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_posts(request):
    """Get all published blog posts"""
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_post_by_slug(request, slug):
    """Get a single blog post by slug"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    serializer = BlogPostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blog_categories(request):
    """Get all blog categories"""
    categories = BlogCategory.objects.all()
    serializer = BlogCategorySerializer(categories, many=True)
    return Response(serializer.data)