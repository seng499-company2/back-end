from preferences.serializers import PreferencesSerializer
from preferences.models import Preferences
import json
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

request: HttpRequest
professor_id: str
preferences_record = Preferences.objects.get(professor__user__username='juliaa')
serializer = PreferencesSerializer(preferences_record)

#json.dumps(serializer.data)