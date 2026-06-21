# home/models.py
from django.db import models

class HomeHero(models.Model):
    """Hero section content (ပင်မစာမျက်နှာ အပေါ်ဆုံးအပိုင်း)"""
    badge_text = models.CharField(max_length=100, default="We design first")
    title_prefix = models.CharField(max_length=100, default="lwal")
    title_highlight = models.CharField(max_length=100, default="kuu")
    subtitle = models.CharField(max_length=500, default="from generative models to agentic automation")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hero Section - {self.updated_at}"

class HomeStat(models.Model):
    """Statistics numbers (572k, 468k, etc.)"""
    label = models.CharField(max_length=100)  # Projects, Clients, Reviews, Downloads
    number = models.CharField(max_length=50)  # 572, 468, 1.5, 794
    suffix = models.CharField(max_length=10, default="k")  # k, M, etc.
    icon_name = models.CharField(max_length=50, default="TrendingUp")  # Icon name
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.label}: {self.number}{self.suffix}"

class HomeService(models.Model):
    """Services section (Web Development, Mobile Apps, UI/UX Design)"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_name = models.CharField(max_length=50, default="Globe")  # Icon name
    image = models.ImageField(upload_to='home/services/', null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class HomeExploreCard(models.Model):
    """Explore section (Shots, Hire Talent, Get Hired, Community)"""
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon_name = models.CharField(max_length=50, default="Sparkles")
    link = models.CharField(max_length=255, blank=True, default="/")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class HomeCTASetting(models.Model):
    """CTA Section content"""
    title = models.CharField(max_length=255, default="Ready to Build Something Great?")
    description = models.CharField(max_length=500, default="Get 20% (up to $100) off your first payment for a limited time!")
    button1_text = models.CharField(max_length=100, default="Start Your Project")
    button1_link = models.CharField(max_length=255, default="/contact")
    button2_text = models.CharField(max_length=100, default="Explore Services")
    button2_link = models.CharField(max_length=255, default="/services")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CTA Settings - {self.updated_at}"

class HomeImage(models.Model):
    """ပုံများ upload လုပ်ရန်"""
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='home/images/')
    section = models.CharField(max_length=100, default='hero')  # hero, services, explore
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"