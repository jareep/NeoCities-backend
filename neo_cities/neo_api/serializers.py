from rest_framework import serializers
from neo_api.models import Resource, Event, Threshold, Role, ResourceDepot, Scenario, Briefing, Score, Participant, \
    Session, \
    Action


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'icon')
        read_only_fields = ['id']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'icon', 'start_time', 'description', 'details')
        read_only_fields = ['id']


class ThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Threshold
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class ResourceDepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceDepot
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class BriefingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Briefing
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = model._meta.get_fields()
        read_only_fields = ['id']


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = model._meta.get_fields()
        read_only_fields = ['id']
