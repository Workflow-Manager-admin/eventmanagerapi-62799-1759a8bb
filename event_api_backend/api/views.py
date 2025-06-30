from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer


# Health check endpoint (no auth)
@api_view(['GET'])
def health(request):
    print(self.request.scheme)
    print(self.request.get_host())
    return Response({"message": "Server is up!"})



# PUBLIC_INTERFACE
class EventListCreateView(generics.ListCreateAPIView):
    """
    List all events or create a new event.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all().order_by("-start_time")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


# PUBLIC_INTERFACE
class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an event instance.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_at=None)  # auto_now should handle

    def perform_destroy(self, instance):
        instance.delete()
