from rest_framework import serializers
from .models import World
 
# create a serializer
class WorldSerializer(serializers.HyperlinkedModelSerializer):
    # initialize model and fields you want to serialize
    class Meta:
        model = World
        fields = ['name', 'population']

