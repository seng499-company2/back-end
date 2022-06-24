from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    #/preferences/{professor-id}
    path('preferences/<str:professor_id>/', views.PreferencesRecord.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)