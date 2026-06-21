# social/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Profile
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/<str:username>/', views.user_profile, name='user-profile'),
    path('follow/<str:username>/', views.follow_user, name='follow-user'),
    
    # Posts
    path('posts/', views.posts, name='posts'),
    path('posts/public/', views.public_posts, name='public-posts'),
    path('posts/<int:pk>/', views.post_detail, name='post-detail'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    
    # Comments
    path('posts/<int:pk>/comments/', views.post_comments, name='post-comments'),
    path('posts/<int:pk>/comments/add/', views.add_comment, name='add-comment'),
    
    # Notifications
    path('notifications/', views.get_notifications, name='notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark-all-read'),
    path('notifications/<int:pk>/delete/', views.delete_notification, name='delete-notification'),
    
    # Admin
    path('auth/verify-admin/', views.verify_admin, name='verify-admin'),
]