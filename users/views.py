import json

from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainSlidingView

import users
from .models import AppUser
from .serializers import AppUserSerializer, UserTokenObtainSlidingSerializer
from .permissions import IsAdmin


class ProfessorsList(APIView):
    """
    Administrator User Management: List all professors, or create a new professor record.
    """
    
    permission_classes = [IsAdmin, IsAuthenticated]

    # (Admin) return all profs within the system.
    def get(self, request):
        print("received GET request to ProfessorsList API Endpoint")
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # get all prof AppUsers **may have to also fetch User parent class + concatenate fields**
        profs_list = AppUser.objects.exclude(prof_type=AppUser.TeachingType.OTHER)
        serializer = AppUserSerializer(profs_list, many=True)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    # (Admin) create a new professor record.
    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        print("received POST request to ProfessorsList API Endpoint")
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        request_data = JSONParser().parse(request)

        #upon Prof creation, manually assert that a password was provided in the request body
        if 'password' not in request_data['user']:
            return HttpResponse("No password was provided for the new Professor account!", status=status.HTTP_400_BAD_REQUEST)

        serializer = AppUserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Professor(APIView):
    """
    Administrator User Management: Update or delete a single professor record.
    """
    
    permission_classes = [IsAdmin, IsAuthenticated]

    # (Admin) update an existing user/professor record.
    def post(self, request: HttpRequest, professor_id: str, format=None) -> HttpResponse:
        print("received POST request to Professors API Endpoint")
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            prof = AppUser.objects.get(user__username=professor_id)
            if prof is None or not isinstance(prof, AppUser):
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except users.models.AppUser.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        request_data = JSONParser().parse(request)
        serializer = AppUserSerializer(prof, data=request_data)
        if serializer.is_valid():
            serializer.update(prof, serializer.validated_data)
            return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an existing user/professor record.
    def delete(self, request: HttpRequest, professor_id: str, format=None) -> HttpResponse:
        print("received DELETE request to Professors API Endpoint")
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            prof = AppUser.objects.get(user__username=professor_id)
        except users.models.AppUser.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        prof.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    

class UserDetail(APIView):
    """
    All User Management: Retrieve logged in user's information.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("received GET request to UserDetail API Endpoint")
        token_user_username = request.user.username
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            appUser = AppUser.objects.get(user__username=token_user_username)
        except users.models.AppUser.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AppUserSerializer(appUser)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)
    
class UserTokenObtainSlidingView(TokenObtainSlidingView):
    """
    Override to use custom serializer class for Login View
    """
    serializer_class = UserTokenObtainSlidingSerializer