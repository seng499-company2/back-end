import json
import courses


from .models import Course
from schedule.Schedule_models import A_Course, A_CourseOffering
from rest_framework.parsers import JSONParser
from .serializers import CourseSerializer
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import status

from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated

from schedule.adapter import course_to_course_offering, add_course_offering_to_schedule



class AllCoursesView(APIView):

    permission_classes = [IsAdmin, IsAuthenticated]

    def get(self, request):
        print("received GET request to AllCoursesView API Endpoint")
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = CourseSerializer(Course.objects, many=True)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    def post(self, request: HttpRequest) -> HttpResponse:
        print("received POST request to AllCoursesView API Endpoint")
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_data = JSONParser().parse(request)
        serializer = CourseSerializer(data=request_data)
        
        if serializer.is_valid():
            course = serializer.create(serializer.validated_data)
            course_offering = course_to_course_offering(course)
            course_offering.save()
            add_course_offering_to_schedule(course, course_offering)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseView(APIView):

    permission_classes = [IsAdmin, IsAuthenticated]

    def get(self, request: HttpRequest, course_code: str):
        print("received GET request to CourseView API Endpoint")
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
        print("received POST request to CourseView API Endpoint")
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
            course = serializer.update(course, serializer.validated_data)
            alg_course_offering = course_to_course_offering(course)
            alg_course_offering.save()
            add_course_offering_to_schedule(course, alg_course_offering)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, course_code: str, format=None) -> HttpResponse:
        print("received DELETE request to CourseView API Endpoint")
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            course = Course.objects.get(course_code=course_code)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        alg_course_offering = course_to_course_offering(course)
        course.delete()
        alg_course_offering.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
