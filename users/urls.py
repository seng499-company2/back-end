from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    #/users
    path('users/', views.ProfessorsList.as_view()),
    #/users/{professor-id}
    path('users/<int:professor_id>/', views.Professor.as_view()),

    path('login/', views.Login.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)