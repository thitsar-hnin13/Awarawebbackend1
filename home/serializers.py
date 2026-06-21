# home/serializers.py
from rest_framework import serializers
from .models import (
    HomeHero, HomeStat, HomeService, 
    HomeExploreCard, HomeCTASetting, HomeImage
)

class HomeHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeHero
        fields = '__all__'

class HomeStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeStat
        fields = '__all__'

class HomeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeService
        fields = '__all__'

class HomeExploreCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeExploreCard
        fields = '__all__'

class HomeCTASettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeCTASetting
        fields = '__all__'

class HomeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeImage
        fields = '__all__'