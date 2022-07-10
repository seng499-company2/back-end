import json
import courses


from .models import Course
from schedule.Schedule_models import A_Course
from rest_framework.parsers import JSONParser
from .serializers import CourseSerializer
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework import status

from .permissions import IsAdmin
from rest_framework.permissions import IsAuthenticated


def get_alg_course(course: Course) -> A_Course:
    try:
        a_course = A_Course.objects.get(code=course.course_code)
    except A_Course.DoesNotExist:
        a_course = A_Course()
    a_course.code = course.course_code
    a_course.title = course.course_title
    a_course.pengRequired = course.pengRequired
    a_course.yearRequired = course.yearRequired
    return a_course


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
            course = serializer.create(serializer.validated_data)
            a_course = get_alg_course(course)
            a_course.save()
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CourseView(APIView):

    permission_classes = [IsAdmin, IsAuthenticated]

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
            course = serializer.update(course, serializer.validated_data)
            alg_course = get_alg_course(course)
            alg_course.save()
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request: HttpRequest, course_code: str, format=None) -> HttpResponse:
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            course = Course.objects.get(course_code=course_code)
        except courses.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        course = course.delete()
        alg_course = get_alg_course(course)
        alg_course.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
