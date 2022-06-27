from django.shortcuts import render
from .models import Course
from .serializers import CourseSerializer
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.views import APIView



class ListCourses(APIView):

    def get(self, request):
            if request.method != "GET":
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
            serializer = CourseSerializer(Courses.objects, many=True)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


    def get(self, request: HttpRequest, course_id: str):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            course = Course.objects.get(Course.id == id)
            if course is None or not isinstance(course, Course):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except course.models.Course.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


# Create your views here.


