from rest_framework import serializers
from neo_api.models import Event


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    icon = serializers.ImageField()
    # start_time = serializers.DateTimeField()
    description = serializers.CharField()
    details = serializers.CharField()

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event

    def update(self, instance, validated_data):
        instance.icon = validated_data.get('icon', instance.email);
        # instance.start_time = validated_data.get('start_time', instance.start_time);
        instance.description = validated_data.get('description', instance.description);
        instance.details = validated_data.get('details', instance.details);
        return instance
