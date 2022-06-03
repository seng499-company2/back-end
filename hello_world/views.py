from rest_framework import viewsets
from .serializers import WorldSerializer
from .models import World
 
class WorldViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing worlds.
    """
    queryset = World.objects.all()
    serializer_class = WorldSerializer