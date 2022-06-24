from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainSlidingView
from . import views

urlpatterns = [
    #/users
    path('users/', views.ProfessorsList.as_view()),
    #/users/{professor-id}
    path('users/<str:professor_id>/', views.Professor.as_view()),
    #/user
    path('user/', views.UserDetail.as_view()),
    path('login/', TokenObtainSlidingView.as_view(), name='token_obtain'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
