from django.shortcuts import render
from rest_framework import viewsets
from helloapi.serializers import MessageSerializer
from helloapi.models import Message


# Create your views here.
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer