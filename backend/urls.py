# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from social import views as social_views  # ဒီ line ကို ထည့်ပါ

def api_home(request):
    return JsonResponse({
        'message': 'Lwal Kuu Tech API is running',
        'endpoints': {
            'projects': '/api/projects/projects/',
            'team': '/api/projects/team/',
            'blog_posts': '/api/blog/posts/',
            'blog_categories': '/api/blog/categories/',
            'contact': '/api/contacts/message/',
            'auth': '/api/auth/',
            'social': '/api/social/',
            'public_posts': '/api/posts/public/',  # ထည့်လိုက်ပါ
        }
    })

# Main urlpatterns
urlpatterns = [
    path('', api_home, name='api-home'),
    path('admin/', admin.site.urls),
    path('api/projects/', include('projects.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/contacts/', include('contacts.urls')),
    path('api/home/', include('home.urls')),
    path('api/auth/', include('accounts.urls')),
    path('api/social/', include('social.urls')),
    
    # Public posts endpoint - ဒီအတိုင်း ထည့်ပါ
    path('api/posts/public/', social_views.public_posts, name='public-posts'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)