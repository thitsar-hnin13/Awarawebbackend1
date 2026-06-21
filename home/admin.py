# home/admin.py
from django.contrib import admin
from .models import (
    HomeHero, HomeStat, HomeService, 
    HomeExploreCard, HomeCTASetting, HomeImage
)

@admin.register(HomeHero)
class HomeHeroAdmin(admin.ModelAdmin):
    list_display = ['badge_text', 'is_active', 'updated_at']
    list_editable = ['is_active']

@admin.register(HomeStat)
class HomeStatAdmin(admin.ModelAdmin):
    list_display = ['label', 'number', 'suffix', 'order']
    list_editable = ['order']

@admin.register(HomeService)
class HomeServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']

@admin.register(HomeExploreCard)
class HomeExploreCardAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']

@admin.register(HomeCTASetting)
class HomeCTASettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'updated_at']
    list_editable = ['is_active']

@admin.register(HomeImage)
class HomeImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'section', 'order', 'created_at']
    list_editable = ['order', 'section']