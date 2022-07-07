from django.contrib import admin
from .Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering

admin.site.register(A_Schedule)
admin.site.register(A_TimeSlot)
admin.site.register(A_CourseSection)
admin.site.register(A_Course)
admin.site.register(A_CourseOffering)
