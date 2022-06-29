from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
)
from . import views

urlpatterns = [
    # GET / schedule / files / {scheduleId}
    # Example: http://localhost:8000/schedule/files/schedule_id/2
    path('files/<str:schedule_id>/<int:company_alg>', views.ScheduleFile.as_view()),

    # GET / schedule / {year - semester}
    # Example: http://localhost:8000/schedule/2022/FALL/2
    path('<int:year>/<str:semester>/<int:requested_company_alg>', views.Schedule.as_view()),

    # POST / schedule / {scheduleId} / {courseId}
    # Example: http://localhost:8000/schedule/schedule_id/course_id/2
    path('<str:schedule_id>/<str:course_id>/<int:company_alg>', views.Schedule.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
