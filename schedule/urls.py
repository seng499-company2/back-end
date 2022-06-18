from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
)
from . import views

urlpatterns = [
    # GET / schedule / {year - semester}
    path('/schedule/<int:year>-<str:semester>-<int:company>', views.Schedule.as_view()),

    # POST / schedule / {scheduleId} / {courseId}
    path('/schedule/<str:schedule_id>/<str:course_id>-<int:company_alg>', views.Schedule.as_view()),

    # GET / schedules / files / {scheduleId}
    path('/schedule/files/<str:schedule_id>-<int:company_alg>', views.Schedule.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
