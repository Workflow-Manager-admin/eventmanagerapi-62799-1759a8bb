from django.contrib import admin
from .models import Event


# PUBLIC_INTERFACE
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Admin registration for Event.
    """
    list_display = ("name", "location", "start_time", "end_time", "created_by")
    search_fields = ("name", "location", "created_by__username")
    list_filter = ("location", "start_time", "created_by")
    ordering = ("-start_time",)
