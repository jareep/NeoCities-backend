from rest_framework import serializers
from neo_api.models import Role, Participant, ResourceDepot, Resource, ResourceEventState, Scenario, Session, Action, Briefing ,Threshold, Message, ChatSession

def get_model_serializer(db_model, field_exceptions = [], depth = 1):
    def clean_field(field):
        return not (field in field_exceptions)


    # Grab the fields we want
    clean_fields = [field.name for field in db_model._meta.get_fields() if clean_field(field.name)]

    # Create the meta class for our serializer class
    meta_data = {"model": db_model, "fields": clean_fields, "read_only_fields": ['id'], "depth": depth}
    if(db_model != Action and db_model != Threshold and db_model != Briefing):
        meta_data["depth"] = 2
    meta_class = type("Meta", (), meta_data)

    # Create the serializer class and return it
    serializer_class = type(db_model.__name__ + "Serializer", (serializers.ModelSerializer,),
                            {"Meta": meta_class})
    return serializer_class

class ResourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resource
        fields = ["icon", 'name']
        read_only_fields = ['id', 'name']
        depth = 3

class RoleSerializer(serializers.ModelSerializer):
    resourcedepot_set = get_model_serializer(ResourceDepot)(many=True)

    class Meta:
        model = Role
        fields = ["resourcedepot_set", "icon", "id", "name"]
        read_only_fields = ['id']
        depth = 3


class ScenarioSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True)

    class Meta:
        model = Scenario
        fields = ["events", "roles"]
        read_only_fields = ['id']
        depth = 4

class SessionSerializer(serializers.ModelSerializer):
    scenario_ran = ScenarioSerializer()

    class Meta:
        model = Session
        fields = ["scenario_ran", "sessionKey"]
        read_only_fields = ['id']
        depth = 4

class ParticipantSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    session = SessionSerializer()

    class Meta:
        model = Participant
        fields = ["name", "token", "session", "score", "role", 'id']
        read_only_fields = ['id']
        depth = 4

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ["text", "chat_session", "participant"]

class ChatSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatSession
        fields = ["message_set", "id"]
        read_only_fields = ['id']
        depth = 2

def get_resource_event_state(event, resource, session):
    # If the resource event state has not been created create it
    try:
        resource_event_state = ResourceEventState.objects.get(session = session, event = event, resource = resource)
    except ResourceEventState.DoesNotExist:
        resource_event_state = ResourceEventState.objects.create(session = session, resource = resource, event = event)

    resource_event_state.save()
    return(resource_event_state)
