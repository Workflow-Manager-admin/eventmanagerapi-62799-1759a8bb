from rest_framework import serializers
from .models import Event


# PUBLIC_INTERFACE
class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for Event objects with full validation.
    """
    created_by = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "location", "start_time", "end_time",
            "created_by", "created_at", "updated_at"
        ]
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate(self, data):
        """
        Validate event times and name uniqueness.
        """
        instance = self.instance
        name = data.get("name") or (instance and instance.name)
        start_time = data.get("start_time") or (instance and instance.start_time)
        end_time = data.get("end_time") or (instance and instance.end_time)
        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError("End time must be after start time.")
        from django.utils import timezone
        if start_time and start_time < timezone.now():
            raise serializers.ValidationError("Start time must be in the future.")
        # Prevent duplicate event names
        qs = Event.objects.filter(name=name)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("An event with this name already exists.")
        return data
