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


def get_auth_errors(request: HttpRequest) -> HttpResponse | None:
    # in a try block because if authenticating with token request.user doesn't even exist
    try:
        # At time of development, Not sure if request.user will be a django.contrib.auth.models
        # or an AppUser. Both cases covered
        caller = request.user.user if isinstance(request.user, AppUser) else request.user
        if (not caller.is_authenticated) or (not caller.is_superuser):
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
    except AttributeError:
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return None


class ProfessorsList(APIView):
    """
    Administrator User Management: List all professors, or create a new professor record.
    """

    # (Admin) return all profs within the system.
    def get(self, request):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        authentication_error = get_auth_errors(request)
        if authentication_error is not None:
            return authentication_error

        # get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
        profs_list = AppUser.objects.filter(user__is_superuser=False)
        serializer = AppUserSerializer(profs_list, many=True)
        return HttpResponse(json.dumps(serializer.data), status=status.HTTP_200_OK)

    # (Admin) create a new professor record.
    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        authentication_error = get_auth_errors(request)
        if authentication_error is not None:
            return authentication_error

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

    # (Admin) update an existing user/professor record.
    def post(self, request: HttpRequest, requested_pk: str, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        authentication_error = get_auth_errors(request)
        if authentication_error is not None:
            return authentication_error

        try:
            prof = AppUser.objects.get(user__username=requested_pk)
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
    def delete(self, request: HttpRequest, requested_pk: str, format=None) -> HttpResponse:
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        authentication_error = get_auth_errors(request)
        if authentication_error is not None:
            return authentication_error
        try:
            prof = AppUser.objects.get(user__username=requested_pk)
        except users.models.AppUser.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        prof.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
