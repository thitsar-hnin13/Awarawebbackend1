from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.get_blog_posts, name='blog-posts'),
    path('posts/<slug:slug>/', views.get_blog_post_by_slug, name='blog-post-detail'),
    path('categories/', views.get_blog_categories, name='blog-categories'),
]