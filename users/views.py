from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status

from .models import AppUser
from .serializers import AppUserSerializer

class ProfessorsList(APIView):
    """
    Administrator User Management: List all professors, or create a new professor record.
    """
    #(Admin) return all profs within the system.
    def get(self, request):
        #get all non-admin AppUsers **may have to also fetch User parent class + concatenate fields**
        profs_list = AppUser.objects.filter(user__is_superuser=False)
        serializer = AppUserSerializer(profs_list, many=True)
        return HttpResponse(serializer.data)

    #(Admin) create a new professor record.
    def post(self, request, format=None):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data, status=status.HTTP_201_CREATED)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Professor(APIView):
    """
    Administrator User Management: Update or delete a single professor record.
    """
    #(Admin) update an existing user/professor record.
    def post(self, request, pk, format=None):
        prof = self.get_object(pk)
        serializer = ProfessorSerializer(prof, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(serializer.data)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete an existing user/professor record.
    def delete(self, request, pk, format=None):
        prof = self.get_object(pk)
        prof.delete()
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