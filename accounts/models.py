# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='accounts_profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    website = models.URLField(blank=True, default='')
    company = models.CharField(max_length=100, blank=True, default='')
    position = models.CharField(max_length=100, blank=True, default='')
    github = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')
    instagram = models.URLField(blank=True, default='')
    facebook = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'accounts_profile'):
        instance.accounts_profile.save()