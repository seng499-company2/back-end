from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status

from .models import AppUser
from .serializers import AppUserSerializer


class ProfessorsList(APIView):
    """
    Administrator User Management: List all professors, or create a new professor record.
    """

    # (Admin) return all profs within the system.
    def get(self, request):
        if request.method != "GET":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # TODO: Check for admin in request

        # get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
        profs_list = AppUser.objects.filter(user__is_superuser=False)
        serializer = AppUserSerializer(profs_list, many=True)
        return HttpResponse(serializer.data, status=status.HTTP_200_OK)

    # (Admin) create a new professor record.
    def post(self, request: HttpRequest, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # TODO: Check for admin in request
        request_data = JSONParser().parse(request)
        serializer = AppUserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Professor(APIView):
    """
    Administrator User Management: Update or delete a single professor record.
    """

    # (Admin) update an existing user/professor record.
    def post(self, request: HttpRequest, requested_pk, format=None) -> HttpResponse:
        if request.method != "POST":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # TODO: Check for admin in request

        prof = AppUser.objects.get(pk=requested_pk)
        if prof is None or not isinstance(prof, AppUser):
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        request_data = JSONParser().parse(request)
        serializer = AppUserSerializer(prof, data=request_data)
        if serializer.is_valid():
            serializer.update(prof, serializer.validated_data)
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete an existing user/professor record.
    def delete(self, request: HttpRequest, requested_pk, format=None):
        if request.method != "DELETE":
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # TODO: Check for admin in request

        # prof = AppUser.objects.filter(username=)
        # if prof is None:

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    '''#(Admin) add a new professor record.
    def create(request):
        if response.method == 'POST':
            prof = User()
        
            article.contents = 'This is the content'
            article.save()

            template = loader.get_template('articles/index.html')
            context = {
                'new_article_id': article.pk,
            }
            return HttpResponse(template.render(context, request))


    #(Admin) update an existing professor's record.
    def update(request, professor_id):
        try:
            user = User.objects.get(pk=user_id)
            user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
            user.save()
        except:
            raise Http404("Professor does not exist!")
        return render(request, 'polls/detail.html', {'question': question})'''
