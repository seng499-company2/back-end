from schedule.Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering


#build TimeSlot objects
t1 = A_TimeSlot(dayOfWeek='MONDAY', timeRange='("12:00","13:00")')
t2 = A_TimeSlot(dayOfWeek='TUESDAY', timeRange='("14:00","15:00")')
t1.save()   #NOTE: Many-to-many relationships cannot be created without saving BOTH entity objects first
t2.save()

#build CourseSection objects
cs1 = A_CourseSection(professor={"id": "mzastre", "name":"Michael Zastre"}, capacity=0)
cs1.save()
cs1.timeSlots.add(t1, t2)

#build Course objects
c1 = A_Course(code="CSC225", title="Algorithms and Data Structures I", pengRequired={"fall": True, "spring": False, "summer": True}, yearRequired=3)
c1.save()

#build CourseOffering objects
co_fall = A_CourseOffering()
co_fall.save()
co_fall.course.add(c1)
co_fall.sections.add(cs1)

co_spring = A_CourseOffering()
co_spring.save()
co_spring.course.add(c1)
co_spring.sections.add(cs1)

co_summer = A_CourseOffering()
co_summer.save()
co_summer.course.add(c1)
co_summer.sections.add(cs1)

#finally, build Schedule object
schedule = A_Schedule()
schedule.save()
schedule.fall.add(co_fall)
schedule.spring.add(co_spring)
schedule.summer.add(co_summer)