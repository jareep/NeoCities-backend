from rest_framework import serializers
# from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, \
#     Session, \
#     Action


#
# models = (Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, \
#     Session, Action)
#
#
# for serializer_model in models:
#     test = type(serializer_model.__name__ + "Serializer", (serializers.ModelSerializer,),
#         {"model": serializer_model,
#         "fields": serializer_model._meta.get_fields(),
#         "read_only_fields": ['id']})
#     self.add(test)

def getModelSerializer(db_model, field_exceptions):

    def clean_field(field):
        return(not (field in field_exceptions))

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
    return(serializer_class)


#
# class ResourceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Resource
#         fields = ('id', 'name', 'icon')
#         read_only_fields = ['id']
#
#
# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = ('id', 'icon', 'start_time', 'description', 'details')
#         read_only_fields = ['id']
#
#
# class ThresholdSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Threshold
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class RoleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class ResourceDepotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ResourceDepot
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class ScenarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Scenario
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class BriefingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Briefing
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class ScoreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Score
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class ParticipantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Participant
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Session
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
#
#
# class ActionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Action
#         fields = model._meta.get_fields()
#         read_only_fields = ['id']
