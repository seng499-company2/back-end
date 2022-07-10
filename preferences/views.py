import json

from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework.parsers import ParseError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.models import AppUser

import preferences
from .models import Preferences
from courses.models import Course
from .serializers import PreferencesSerializer
from .permissions import IsAdmin


class PreferencesRecord(APIView):
    """
    Administrator Preferences: Get a professor's preferences record, or update an existing professor record.
    """
    
    permission_classes = [IsAdmin, IsAuthenticated]

    # (Admin) return the unique Preferences record for a professor.
    def get(self, request: HttpRequest, professor_id: str):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            #Get a Preference record and the full list of Course.code
            preferences_record = Preferences.objects.get(professor__user__username=professor_id)
            course_codes_data = list(Course.objects.values_list('course_code', flat=True))

            if preferences_record is None or not isinstance(preferences_record, Preferences):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except preferences.models.Preferences.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = PreferencesSerializer(preferences_record)
        data = {
            'resource': serializer.data,
            'course_codes': course_codes_data
        }
        return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)

    # (Admin) update the unique Preferences record for a professor.
    def post(self, request: HttpRequest, professor_id: str, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            preferences_record = Preferences.objects.get(professor__user__username=professor_id)
            if preferences_record is None or not isinstance(preferences_record, Preferences):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except preferences.models.Preferences.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        request_data = JSONParser().parse(request)
        serializer = PreferencesSerializer(preferences_record, data=request_data)
        if serializer.is_valid():
            serializer.update(preferences_record, serializer.validated_data)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PreferencesView(APIView): 

    permission_classes = [IsAuthenticated]

    # GET api/preferences
    def get(self, request: HttpRequest) -> HttpResponse: 
        if "GET" != request.method: 
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        professor_id = request.user.username
        try:
            #Get a Preference record and the full list of Course.code
            preferences_model = Preferences.objects.get(professor__user__username=professor_id)
            course_codes_data = list(Course.objects.values_list('course_code', flat=True))
            if preferences_model is None or not isinstance(preferences_model, Preferences):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            serializer = PreferencesSerializer(preferences_model)
            data = {
                'resource': serializer.data,
                'course_codes': course_codes_data
            }
            return HttpResponse(json.dumps(data), status=status.HTTP_200_OK)
        except preferences.models.Preferences.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)


    def save_preferences(self, request_data) -> HttpResponse: 
        serializer = PreferencesSerializer(data=request_data)
        if serializer.is_valid(): 
            serializer.save()
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def update_preferences(self, request_data, preferences_model: Preferences) -> HttpResponse: 
        serializer = PreferencesSerializer(preferences_model, data=request_data)
        if serializer.is_valid():
            serializer.update(preferences_model, serializer.validated_data)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_malicious_request(self, user, request_data): 
        try: 
            malicious_request = user.username != request_data['professor']
            return malicious_request
        except:
            # requests without data or without an associated user are assumed not malicious
            return False
 
    def update_user_form_saved(self, professor_id: str):
            prof: AppUser = AppUser.objects.get(user__username=professor_id)
            prof.is_form_submitted = True
            prof.save()

    # POST api/preferences
    def post(self, request: HttpRequest) -> HttpResponse: 
        if "POST" != request.method: 
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_data = JSONParser().parse(request)
        if self.is_malicious_request(request.user, request_data): 
            return HttpResponse("QUIT TRYING TO EDIT THE PREFERENCES OF OTHER PROFS", status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            # Assign a preferences object to preferences_model, if one already exists
            professor_id = request.user.username
            preferences_model = Preferences.objects.get(professor__user__username=professor_id)
            if preferences_model is None or not isinstance(preferences_model, Preferences):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except preferences.models.Preferences.DoesNotExist:
            response = self.save_preferences(request_data)
            # After saving preferences, update AppUser to reflect saved preferences form
            self.update_user_form_saved(professor_id)
            return response
        response = self.update_preferences(request_data, preferences_model)
        # After updating preferences, update AppUser to reflect saved preferences form
        # Normally redundant(this happens when the form is first saved), 
        # but if an admin creates the preferences object for the prof this is the endpoint they'll hit
        self.update_user_form_saved(professor_id)
        return response
