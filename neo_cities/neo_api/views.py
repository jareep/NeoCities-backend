from django.shortcuts import render
from neo_api.models import Event, Resource
from neo_api.serializers import EventSerializer, ResourceSerializer
from rest_framework import viewsets


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
