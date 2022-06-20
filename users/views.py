import json

from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

import users
from .models import AppUser
from .serializers import AppUserSerializer
from .permissions import IsAdmin


class ProfessorsList(APIView):
    """
    Administrator User Management: List all professors, or create a new professor record.
    """

    permission_classes = [IsAdmin, IsAuthenticated]

    # (Admin) return all profs within the system.
    def get(self, request):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
        profs_list = AppUser.objects.filter(user__is_superuser=False)
        serializer = AppUserSerializer(profs_list, many=True)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    # (Admin) create a new professor record.
    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        request_data = JSONParser().parse(request)
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
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            prof = AppUser.objects.get(user__username=professor_id)
        except users.models.AppUser.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        prof.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
