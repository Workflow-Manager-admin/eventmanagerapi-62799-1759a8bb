from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone


# PUBLIC_INTERFACE
class Event(models.Model):
    """
    Event model represents an event in the system.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="events"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # PUBLIC_INTERFACE
    def clean(self):
        """Custom validation to ensure end_time > start_time and non-past start."""
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')
        if self.start_time < timezone.now():
            raise ValidationError('Start time must be in the future.')

    # PUBLIC_INTERFACE
    def save(self, *args, **kwargs):
        """Override to call clean() for validation."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.start_time.date()})"
