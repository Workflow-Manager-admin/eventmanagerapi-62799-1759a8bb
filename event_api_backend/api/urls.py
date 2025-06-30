from django.urls import path
from .views import health, EventListCreateView, EventRetrieveUpdateDestroyView

urlpatterns = [
    path('health/', health, name='Health'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
]
