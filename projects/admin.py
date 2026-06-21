from django.contrib import admin
from .models import Project, TeamMember

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order']
    list_editable = ['order']
    search_fields = ['name', 'role']