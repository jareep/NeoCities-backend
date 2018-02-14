from django.shortcuts import render
from neo_api.models import Event
from neo_api.serializers import EventSerializer
from rest_framework import viewsets

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
