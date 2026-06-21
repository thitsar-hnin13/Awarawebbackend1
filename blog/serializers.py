from rest_framework import serializers
from .models import BlogCategory, BlogPost

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']

class BlogPostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author', 'author_name', 'category', 
                  'category_name', 'thumbnail', 'content', 'excerpt', 'tags', 
                  'created_at', 'is_published']