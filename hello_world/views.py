from rest_framework import generics
from .serializers import WorldSerializer
from .models import World
 

class ListWorldView(generics.ListAPIView):
    # define queryset
    queryset = World.objects.all()
    serializer_class = WorldSerializer
