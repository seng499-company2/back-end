from django.shortcuts import render
from .models import CourseSerializer
from .serializers import 
from django.http import HttpResponse
from django.http import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView



class ListCourses(APIView):

    def get(self, request):
            if request.method != "GET":
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
            serializer = AppUserSerializer(Courses.objects, many=True)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)


# Create your views here.


