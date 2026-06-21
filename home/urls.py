# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.get_home_data, name='home-data'),
    path('images/', views.manage_images, name='manage-images'),
    path('images/<int:pk>/', views.manage_image_detail, name='image-detail'),
]