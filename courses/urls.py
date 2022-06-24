from django.urls import include, path

from . import views


urlpatterns = [
    #/courses
    path('courses/', views.ListCourses.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)