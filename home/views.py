# home/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import (
    HomeHero, HomeStat, HomeService, 
    HomeExploreCard, HomeCTASetting, HomeImage
)
from .serializers import (
    HomeHeroSerializer, HomeStatSerializer, HomeServiceSerializer,
    HomeExploreCardSerializer, HomeCTASettingSerializer, HomeImageSerializer
)

@api_view(['GET'])
def get_home_data(request):
    """Get all home page data"""
    hero = HomeHero.objects.filter(is_active=True).first()
    stats = HomeStat.objects.all()
    services = HomeService.objects.all()
    explore_cards = HomeExploreCard.objects.all()
    cta = HomeCTASetting.objects.filter(is_active=True).first()
    images = HomeImage.objects.all()
    
    return Response({
        'hero': HomeHeroSerializer(hero).data if hero else None,
        'stats': HomeStatSerializer(stats, many=True).data,
        'services': HomeServiceSerializer(services, many=True).data,
        'explore_cards': HomeExploreCardSerializer(explore_cards, many=True).data,
        'cta': HomeCTASettingSerializer(cta).data if cta else None,
        'images': HomeImageSerializer(images, many=True).data,
    })

@api_view(['GET', 'POST'])
def manage_images(request):
    """Get all images or upload new image"""
    if request.method == 'GET':
        images = HomeImage.objects.all().order_by('order')
        serializer = HomeImageSerializer(images, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = HomeImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def manage_image_detail(request, pk):
    """Update or delete specific image"""
    try:
        image = HomeImage.objects.get(pk=pk)
    except HomeImage.DoesNotExist:
        return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = HomeImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        image.delete()
        return Response({'message': 'Image deleted'}, status=status.HTTP_204_NO_CONTENT)