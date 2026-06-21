from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer

@api_view(['GET', 'POST'])
def submit_contact(request):
    if request.method == 'GET':
        return Response({
            'message': 'Contact API is working. Send POST request to submit message.',
            'fields': ['name', 'email', 'subject', 'message']
        })
    
    elif request.method == 'POST':
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Message sent successfully! We will get back to you soon.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)