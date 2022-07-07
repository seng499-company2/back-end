from schedule.Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering
from schedule.Schedule_serializers import A_ScheduleSerializer


#script to build and serialize a full sample Schedule object into Python-native data types.

#create timeslots, then save to DB
t1 = A_TimeSlot.objects.create(dayOfWeek='MONDAY', timeRange=["12:00","13:00"])
t2 = A_TimeSlot.objects.create(dayOfWeek='TUESDAY', timeRange=["13:00","14:00"])
t3 = A_TimeSlot.objects.create(dayOfWeek='WEDNESDAY', timeRange=["11:00","12:00"])
t4 = A_TimeSlot.objects.create(dayOfWeek='THURSDAY', timeRange=["13:00","15:00"])
t1.save()
t2.save()
t3.save()
t4.save()

#create courses, then save to DB
# ** Note: models.JSONField() attributes accept a non-stringified Python-valid dictionary **
course1 = A_Course.objects.create(code="CSC226",
    title="Algorithms 1",
    pengRequired={"fall": True, "spring": False, "summer": True},
    yearRequired=2
)
course2 = A_Course.objects.create(code="SENG275",
    title="Testing 1",
    pengRequired={"fall": False, "spring": True, "summer": True},
    yearRequired=2
)
course1.save()
course2.save()

#create course sections, then save to DB
courseSection1 = A_CourseSection.objects.create(professor={"id": 1, "name": "Mike Zastre"},
    capacity=0
)
courseSection2 = A_CourseSection.objects.create(professor={"id": 2, "name": "Bill Bird"},
    capacity=0
)
courseSection1.save()
courseSection2.save()

#...then associate TimeSlot objects (Many-to-Many)
courseSection1.timeSlots.set([t1, t2])
courseSection2.timeSlots.set([t3, t4])

#create course offerings (with associated Course object foreign key (Many-to-One)), then save to DB
courseOffering1 = A_CourseOffering.objects.create(course=course1)
courseOffering2 = A_CourseOffering.objects.create(course=course2)
courseOffering1.save()
courseOffering2.save()

#...then associate CourseSection objects (Many-to-Many)
courseOffering1.sections.set([courseSection1, courseSection2])
courseOffering2.sections.set([courseSection2])

#create a schedule, thne save to DB
schedule = A_Schedule.objects.create()
schedule.save()

#...then associate CourseOffering objects (Many-to-Many)
schedule.fall.set([courseOffering1, courseOffering2])
schedule.spring.set([courseOffering2])
schedule.summer.set([courseOffering1])

#finally, serialize the full object into Python-native data types
serializer = A_ScheduleSerializer(instance=schedule)

'''
Retrieving data object:
    - serializer.data : returns Python-native data object (Python dicts)
    - json.dumps(serializer.data) : returns JSON-converted data object
'''