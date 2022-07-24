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

from schedule.adapter import add_course_offering_to_schedule, \
    course_to_summer_course_offering, course_to_spring_course_offering, course_to_fall_course_offering

from users.models import AppUser
from preferences.models import Preferences
from preferences.serializers import PreferencesSerializer


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
            align_course_models(course)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def align_course_models(course):
    alg_course_offering_fall = course_to_fall_course_offering(course)
    alg_course_offering_fall.save()
    alg_course_offering_spring = course_to_spring_course_offering(course)
    alg_course_offering_spring.save()
    alg_course_offering_summer = course_to_summer_course_offering(course)
    alg_course_offering_summer.save()
    add_course_offering_to_schedule(alg_course_offering_fall, "fall")
    add_course_offering_to_schedule(alg_course_offering_spring, "spring")
    add_course_offering_to_schedule(alg_course_offering_summer, "summer")


class CourseView(APIView):

    permission_classes = [IsAdmin, IsAuthenticated]

    def get(self, request: HttpRequest, course_code: str):
        print("received GET request to CourseView API Endpoint")
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            course = Course.objects.get(course_code=course_code)
            willing_profs_obj = Preferences.objects.filter(courses_preferences__contains={course_code: {"willingness":2}})
            very_willing_profs_obj = Preferences.objects.filter(courses_preferences__contains={course_code: {"willingness": 3}})

            preferences_data = {}

            for obj1 in willing_profs_obj.all():

                willing_json = {}
                willing_json["username"] = obj1.professor.user.username
                willing_json["name"] = obj1.professor.user.first_name + ' ' + obj1.professor.user.last_name
                willing_json["willingness"] = 2
                preferences_data[obj1.professor.user.id] = willing_json

            for obj2 in very_willing_profs_obj.all():

                very_willing_json = {}
                very_willing_json["username"] = obj2.professor.user.username
                very_willing_json["name"] = obj2.professor.user.first_name + ' ' + obj2.professor.user.last_name
                very_willing_json["willingness"] = 3
                preferences_data[obj2.professor.user.id] = very_willing_json

            if course is None or not isinstance(course, Course):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        result = {'Course':serializer.data, 'willingProfessors': preferences_data}
        return HttpResponse(json.dumps(result), status=status.HTTP_200_OK)

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
            align_course_models(course)
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
        alg_course_offering = course_to_fall_course_offering(course)
        alg_course_offering.delete()
        alg_course_offering = course_to_spring_course_offering(course)
        alg_course_offering.delete()
        alg_course_offering = course_to_summer_course_offering(course)
        alg_course_offering.delete()
        course.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
