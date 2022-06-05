from django.urls import include, path

from . import views

urlpatterns = [
    #/users
    path('', views.index, name='index'),
    #/users/{professor-id}
    path('<int:professor_id>/', views.professor, name='professor')
]