import json
import courses

import uuid

from django.shortcuts import render
from .models import Course
from rest_framework.parsers import JSONParser
from .serializers import CourseSerializer
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import status

from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated



class AllCoursesView(APIView):

    permission_classes = [IsAdmin, IsAuthenticated]

    def get(self, request):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = CourseSerializer(Course.objects, many=True)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    
    
    def post(self, request: HttpRequest) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_data = JSONParser().parse(request)
        serializer = CourseSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CourseView(APIView):

    permission_classes = [IsAdmin, IsAuthenticated]

    def get(self, request: HttpRequest, course_code: str, section: str):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            course = Course.objects.get(course_code=course_code, section=section)
            if course is None or not isinstance(course, Course):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, course_code: str, section: str, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            course = Course.objects.get(course_code=course_code, section=section)
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

    
    def delete(self, request: HttpRequest, course_code: str, section: str, format=None) -> HttpResponse:
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            course = Course.objects.get(course_code=course_code, section=section)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
