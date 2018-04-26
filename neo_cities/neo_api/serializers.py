from rest_framework import serializers
from neo_api.models import Role, Participant, ResourceDepot, Resource, ResourceEventState

def get_model_serializer(db_model, field_exceptions = []):
    def clean_field(field):
        return not (field in field_exceptions)

    # Grab the fields we want
    clean_fields = [field.name for field in db_model._meta.get_fields() if clean_field(field.name)]

    # Create the meta class for our serializer class
    meta_class = type("Meta", (),
                      {"model": db_model,
                       "fields": clean_fields,
                       "read_only_fields": ['id']})

    # Create the serializer class and return it
    serializer_class = type(db_model.__name__ + "Serializer", (serializers.ModelSerializer,),
                            {"Meta": meta_class})
    return serializer_class

class ResourceSerializer(serializers.ModelSerializer):
    resourcedepot_set = get_model_serializer(ResourceDepot)

    class Meta:
        model = Resource
        fields = ["icon", 'name']
        read_only_fields = ['id', 'name']
        depth = 3

class RoleSerializer(serializers.ModelSerializer):
    resourcedepot_set = get_model_serializer(ResourceDepot)

    class Meta:
        model = Role
        fields = ["resourcedepot_set", "icon"]
        read_only_fields = ['id', "resourcedepot_set"]
        depth = 3


class ParticipantSerializer(serializers.ModelSerializer):
    role = RoleSerializer

    class Meta:
        model = Participant
        fields = ["name", "token", "session", "role", "score"]
        read_only_fields = ['id']
        depth = 4

def get_resource_event_state(event, resource, session):
    # If the resource event state has not been created create it
    try:
        resource_event_state = ResourceEventState.objects.get(session = session, event = event, resource = resource)
    except ResourceEventState.DoesNotExist:
        resource_event_state = ResourceEventState.objects.create(session = session, resource = resource, event = event)
    resource_event_state.save()
    return(resource_event_state)
