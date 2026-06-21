from rest_framework import serializers
from .models import Project, TeamMember

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'bio', 'image', 'email', 
                  'github_link', 'linkedin_link', 'skills', 'order']