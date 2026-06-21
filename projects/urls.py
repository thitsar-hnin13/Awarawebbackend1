from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='projects'),
    path('team/', views.team_list, name='team'),
]