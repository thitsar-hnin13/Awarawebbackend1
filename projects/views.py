from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project, TeamMember
from .serializers import ProjectSerializer, TeamMemberSerializer

@api_view(['GET'])
def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def team_list(request):
    members = TeamMember.objects.all().order_by('order', 'name')
    serializer = TeamMemberSerializer(members, many=True)
    return Response(serializer.data)