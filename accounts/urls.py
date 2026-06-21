# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('me/', views.get_current_user, name='current-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Profile
    path('profile/', views.my_profile, name='my-profile'),
    path('upload-avatar/', views.upload_avatar, name='upload-avatar'),
    path('upload-cover/', views.upload_cover, name='upload-cover'),
    path('change-password/', views.change_password, name='change-password'),
    path('dashboard/', views.dashboard_stats, name='dashboard'),
]