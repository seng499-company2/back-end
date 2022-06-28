import json
import courses

from django.shortcuts import render
from .models import Course
from rest_framework.parsers import JSONParser
from .serializers import CourseSerializer
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import status




class AllCoursesView(APIView):

    def get(self, request):
            if request.method != "GET":
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
            serializer = CourseSerializer(Course.objects, many=True)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    
    
    def post(self, request: HttpRequest, course_code: str, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_data = JSONParser().parse(request)
        serializer = CourseSerializer(course, data=request_data)
        if serializer.is_valid():
            
            serializer.update(course, serializer.validated_data)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CourseView(APIView):
    def get(self, request: HttpRequest, course_code: str):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            course = Course.objects.get(course_code=course_code)
            if course is None or not isinstance(course, Course):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, course_code: str, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            course = Course.objects.get(course_code=course_code)
            if course is None or not isinstance(course, Course):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        request_data = JSONParser().parse(request)
        serializer = CourseSerializer(course, data=request_data)
        if serializer.is_valid():

            serializer.update(course, serializer.validated_data)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request: HttpRequest, course_code: str, format=None) -> HttpResponse:
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            course = Course.objects.get(course_code=course_code)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


# Create your views here.




    # (Admin) return the unique Preferences record for a professor.
    # def get(self, request: HttpRequest, professor_id: str):
    #     if request.method != "GET":
    #         return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     try:
    #         preferences_record = Preferences.objects.get(professor__user__username=professor_id)
    #         if preferences_record is None or not isinstance(preferences_record, Preferences):
    #             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    #     except preferences.models.Preferences.DoesNotExist:
    #         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    #     serializer = PreferencesSerializer(preferences_record)
    #     return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    # # (Admin) update the unique Preferences record for a professor.
    # def post(self, request: HttpRequest, professor_id: str, format=None) -> HttpResponse:
    #     if request.method != "POST":
    #         return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #     try:
    #         preferences_record = Preferences.objects.get(professor__user__username=professor_id)
    #         if preferences_record is None or not isinstance(preferences_record, Preferences):
    #             return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    #     except preferences.models.Preferences.DoesNotExist:
    #         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    #     request_data = JSONParser().parse(request)
    #     serializer = PreferencesSerializer(preferences_record, data=request_data)
    #     if serializer.is_valid():
    #         serializer.update(preferences_record, serializer.validated_data)
    #         return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
    #     return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)