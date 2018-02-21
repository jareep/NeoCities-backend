from django.shortcuts import render
from neo_api.models import Event, Resource
from neo_api.serializers import getModelSerializer
from rest_framework import viewsets

# These are field exceptions for every model serializer
field_exceptions = ["scenario", "action"]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = getModelSerializer(Event, field_exceptions + ["threshold"])


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = getModelSerializer(Resource, field_exceptions + ["threshold" ,"event", "role", "resourcedepot"])



# def getModelView(db_model, field_exceptions):
#
#     def clean_field(field):
#         return(not (field in field_exceptions))
#
#     # Grab the fields we want
#     clean_fields = [field.name for field in db_model._meta.get_fields() if clean_field(field.name)]
#
#     # Create the serializer class and return it
#     serializer_class = type(db_model.__name__ + "ViewSet", (viewsets.ModelViewSet,),
#         {queryset: db_model.objects.all()})
#     return(serializer_class)
