# social/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Share

# Profile Admin
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at')
    search_fields = ('user__username',)
    
    def follower_count(self, obj):
        return obj.follower_count
    follower_count.short_description = 'Followers'

# Post Admin  
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_preview', 'like_count', 'created_at')
    search_fields = ('user__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:50] if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def like_count(self, obj):
        return obj.like_count
    like_count.short_description = 'Likes'

# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content_preview', 'created_at')
    search_fields = ('user__username', 'content')
    
    def content_preview(self, obj):
        return obj.content[:40] if len(obj.content) > 40 else obj.content
    content_preview.short_description = 'Comment'

# Share Admin
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    search_fields = ('user__username',)

# User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

# Register models
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Share, ShareAdmin)

# Register User (unregister default first)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, UserAdmin)