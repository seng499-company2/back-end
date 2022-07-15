import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scheduler.settings")

import django
django.setup()

from django.core.management import call_command

import csv
import pprint
import json
import os
from enum import Enum

from schedule.Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering
from django.contrib.auth.models import User
from users.models import AppUser
from preferences.models import Preferences

#CSV files containing relevant to be parsed
SCHEDULES_CSV_FILE = 'schedule_courses.csv' #TODO
PROFESSORS_CSV_FILE = '' #TODO
HISTORICAL_CAPACITIES_CSV_FILE = '' #TODO

#The default Professor account password to be used for each new prof account
DEFAULT_PROF_ACCOUNT_PASSWORD = 'professor123'

#maps CSV boolean types to Python T/F
BOOLEAN_MAP = {
    'TRUE': True,
    'FALSE': False,
    '': None
}

#maps Professor's facultyType to AppUser.TEACHING_TYPE enums
FACULTY_TYPE_MAP = {
    'RESEARCH': AppUser.TeachingType.RESEARCH_PROF,
    'TEACHING': AppUser.TeachingType.TEACHING_PROF,
    '': AppUser.TeachingType.OTHER
} 

class CSV_COLUMNS(Enum):
    SEMESTER = 0
    CODE = 1
    TITLE = 2
    PENG_REQUIRED_FALL = 3
    PENG_REQUIRED_SPRING = 4
    PENG_REQUIRED_SUMMER = 5
    YEAR_REQUIRED = 6
    NUM_SECTIONS = 7
    
    SECTION1_PROF_ID = 8
    SECTION1_PROF_NAME = 9
    SECTION1_CAPACITY = 10
    SECTION1_DAYS_OF_WEEK = 11
    SECTION1_TIME_RANGE = 12

    SECTION2_PROF_ID = 13
    SECTION2_PROF_NAME = 14
    SECTION2_CAPACITY = 15
    SECTION2_DAYS_OF_WEEK = 16
    SECTION2_TIME_RANGE = 17

class PROF_CSV_COLUMNS(Enum):
    ID = 0
    FULL_NAME = 1
    IS_PENG = 2
    FACULTY_TYPE = 3
    TEACHING_OBLIGATIONS = 4
    FALL_PREFERRED_TIMES_MONDAY = 5
    FALL_PREFERRED_TIMES_TUESDAY = 6
    FALL_PREFERRED_TIMES_WEDNESDAY = 7
    FALL_PREFERRED_TIMES_THURSDAY = 8
    FALL_PREFERRED_TIMES_FRIDAY = 9
    SPRING_PREFERRED_TIMES_MONDAY = 10
    SPRING_PREFERRED_TIMES_TUESDAY = 11
    SPRING_PREFERRED_TIMES_WEDNESDAY = 12
    SPRING_PREFERRED_TIMES_THURSDAY = 13
    SPRING_PREFERRED_TIMES_FRIDAY = 14
    SUMMER_PREFERRED_TIMES_MONDAY = 15
    SUMMER_PREFERRED_TIMES_TUESDAY = 16
    SUMMER_PREFERRED_TIMES_WEDNESDAY = 17
    SUMMER_PREFERRED_TIMES_THURSDAY = 18
    SUMMER_PREFERRED_TIMES_FRIDAY = 19
    FALL_NUM_PREFERRED_COURSES = 20
    SPRING_NUM_PREFERRED_COURSES = 21
    SUMMER_NUM_PREFERRED_COURSES = 22
    PREFERRED_NON_TEACHING_SEMESTER = 23
    PREFERRED_COURSE_DAY_SPREADS = 24 


def get_days_of_the_week(days_str):
    days_map = {
        'M' : 'MONDAY',
        'T' : 'TUESDAY',
        'W' : 'WEDNESDAY',
        'Th' : 'THURSDAY',
        'F' : 'FRIDAY'
    }
    
    days_list = []
    
    i = 0
    while i < len(days_str):
        if i <= len(days_str) - 2 and days_str[i] == 'T' and days_str[i+1] == 'h':
            days_list.append(days_map['Th'])
            i += 2 # skip both 'T' and 'h'
            continue
        
        days_list.append(days_map[days_str[i]])
        i += 1
        
    return days_list
        

# Converts the input Schedule-object-related data (Courses +++) CSV into Django model instances stored in the DB.
# Queries are performed to the DB to create objects & associate them with the correct relationships to other models.
def parse_schedules_data(csv_file):
    with open(csv_file) as schedules_data_csv:
        csv_reader = csv.reader(schedules_data_csv, delimiter=',')

        #skip the header rows
        next(csv_reader)
        next(csv_reader)

        #get CSV data into memory (list of rows)
        csv_list = []
        for row in csv_reader:
            csv_row = list(row)
            csv_list.append(csv_row)

        #Step 1 - build TimeSlot objects
        for row in csv_list:
            #handling TimeSlots for course with 1 section
            if row[CSV_COLUMNS.SECTION1_TIME_RANGE.value]:
                
                #parse the DaysOfTheWeek CSV string into distinct enum values + TimeRange splittings
                days_list = get_days_of_the_week(row[CSV_COLUMNS.SECTION1_DAYS_OF_WEEK.value])
                time_range = str(row[CSV_COLUMNS.SECTION1_TIME_RANGE.value]).split('~')

                #create Django models & store to DB
                for day in days_list:
                    _, _ = A_TimeSlot.objects.get_or_create(
                        dayOfWeek=day,
                        timeRange=time_range
                    )

            #extra case - handling TimeSlots for course with 2 sections
            if int(row[CSV_COLUMNS.NUM_SECTIONS.value]) == 2:
                if row[CSV_COLUMNS.SECTION2_TIME_RANGE.value]:
                    
                    #parse the DaysOfTheWeek CSV string into distinct enum values + TimeRange splittings
                    days_list = get_days_of_the_week(row[CSV_COLUMNS.SECTION2_DAYS_OF_WEEK.value])
                    time_range = str(row[CSV_COLUMNS.SECTION2_TIME_RANGE.value]).split('~')

                    #create Django models & store to DB
                    #using try-except here as we cannot guarantee that all fields will be unique for the same course!
                    for day in days_list:
                        _, _ = A_TimeSlot.objects.get_or_create(
                            dayOfWeek=day,
                            timeRange=time_range
                        )


        #Step 2 - build Course objects
        for row in csv_list:
            course_code = row[CSV_COLUMNS.CODE.value]
            title = row[CSV_COLUMNS.TITLE.value]
            peng_required = {
                "fall": BOOLEAN_MAP[row[CSV_COLUMNS.PENG_REQUIRED_FALL.value]],
                "spring": BOOLEAN_MAP[row[CSV_COLUMNS.PENG_REQUIRED_SPRING.value]],
                "summer": BOOLEAN_MAP[row[CSV_COLUMNS.PENG_REQUIRED_SUMMER.value]]
            }
            year_required = int(row[CSV_COLUMNS.YEAR_REQUIRED.value])

            #create Django models & store to DB
            _, _ = A_Course.objects.get_or_create(
                code=course_code,
                title=title,
                pengRequired=peng_required,
                yearRequired=year_required
            )

            
        #Step 3 - build CourseSection objects *(For both Dynamic + Static courses)*
        #store CourseSections objects in memory for easy access
        course_sections_list = []

        for row in csv_list:
            #handling of Section 1                
            if row[CSV_COLUMNS.SECTION1_PROF_ID.value]:
                professor = {
                    "id" : row[CSV_COLUMNS.SECTION1_PROF_ID.value] ,
                    "name" : row[CSV_COLUMNS.SECTION1_PROF_NAME.value]
                }
            else:
                professor = None
            
            if row[CSV_COLUMNS.SECTION1_CAPACITY.value]:
                capacity = int(row[CSV_COLUMNS.SECTION1_CAPACITY.value])
            else:
                capacity = 0

            #forced creation of Django model & store to DB
            courseSection1 = A_CourseSection.objects.create(
                professor=professor,
                capacity=capacity
            )
            courseSection1.save()

            #create the TimeSlots many-to-many relationship, if exists
            if row[CSV_COLUMNS.SECTION1_DAYS_OF_WEEK.value] and row[CSV_COLUMNS.SECTION1_TIME_RANGE.value]:
                days_list = get_days_of_the_week(row[CSV_COLUMNS.SECTION1_DAYS_OF_WEEK.value])
                time_range = str(row[CSV_COLUMNS.SECTION1_TIME_RANGE.value]).split('~')
                time_slots = []
                for day in days_list:
                    #get TimeSlot obj
                    obj, _ = A_TimeSlot.objects.get_or_create(
                        dayOfWeek=day,
                        timeRange=time_range
                    )

                    #associate the TimeSlot
                    time_slots.append(obj)

                courseSection1.timeSlots.set(time_slots)
            course_sections_list.append(courseSection1)
            
            #handling of Section 2, if exists
            if int(row[CSV_COLUMNS.NUM_SECTIONS.value]) == 2:
                if row[CSV_COLUMNS.SECTION2_PROF_ID.value]:
                    professor = {
                        "id" : row[CSV_COLUMNS.SECTION2_PROF_ID.value] ,
                        "name" : row[CSV_COLUMNS.SECTION2_PROF_NAME.value]
                    }
                else:
                    professor = None
                
                if row[CSV_COLUMNS.SECTION2_CAPACITY.value]:
                    capacity = int(row[CSV_COLUMNS.SECTION2_CAPACITY.value])
                else:
                    capacity = 0

                #forced creation of Django model & store to DB
                courseSection2 = A_CourseSection.objects.create(
                    professor=professor,
                    capacity=capacity
                )
                courseSection2.save()

                #create the TimeSlots many-to-many relationship, if exists
                if row[CSV_COLUMNS.SECTION2_DAYS_OF_WEEK.value] and row[CSV_COLUMNS.SECTION2_TIME_RANGE.value]:
                    days_list = get_days_of_the_week(row[CSV_COLUMNS.SECTION2_DAYS_OF_WEEK.value])
                    time_range = str(row[CSV_COLUMNS.SECTION2_TIME_RANGE.value]).split('~')
                    time_slots = []
                    for day in days_list:
                        #get TimeSlot obj
                        obj, _ = A_TimeSlot.objects.get_or_create(
                            dayOfWeek=day,
                            timeRange=time_range
                        )

                        #associate the TimeSlot
                        time_slots.append(obj)

                    courseSection2.timeSlots.set(time_slots)
                course_sections_list.append(courseSection2)
        

        #Step 4 - build CourseOffering objects
        fall_offerings = []
        spring_offerings = []
        summer_offerings = []

        #index to traverse the CourseSections list
        i = 0
        for row in csv_list:
            #get associated Course object foreign key to create CourseOffering, then save to DB
            course_code = row[CSV_COLUMNS.CODE.value]
            course_obj = A_Course.objects.get(code=course_code)

            if row[CSV_COLUMNS.CODE.value] and course_obj is not None:
                courseOffering = A_CourseOffering.objects.create(course=course_obj)
                courseOffering.save()

                #get the associated CourseSection(s) for many-to-many (in memory)
                courseOffering.sections.add(course_sections_list[i])
                i += 1
                if int(row[CSV_COLUMNS.NUM_SECTIONS.value]) == 2:
                    courseOffering.sections.add(course_sections_list[i])
                    i += 1

                #finally, save the CourseOffering in memory to the correct semester
                if row[CSV_COLUMNS.SEMESTER.value] == 'fall':
                    fall_offerings.append(courseOffering)
                elif row[CSV_COLUMNS.SEMESTER.value] == 'spring':
                    spring_offerings.append(courseOffering)
                elif row[CSV_COLUMNS.SEMESTER.value] == 'summer':
                    summer_offerings.append(courseOffering)


        #Step 5 - build the final Schedule object
        schedule = A_Schedule.objects.create()
        schedule.save()

        #build fall, spring, and summer CourseOffering[] lists
        for offering in fall_offerings:
            schedule.fall.add(offering)
        for offering in spring_offerings:
            schedule.spring.add(offering)
        for offering in summer_offerings:
            schedule.summer.add(offering)

        #DB should contain an entire, correctly-associated Schedule object now, that should be retrievable & serializable via:
        #   serializer = A_ScheduleSerializer(instance=schedule)
        #   serializer.data
        #       To replace OrderedDicts --> dicts, use: json.loads(json.dumps(serializer.data))

    return


def generate_account_fields(full_name):
    #build netlinkID: first letter of firstname + entire lastname
    names = full_name.split()
    netlink_id = str((names[0][0] + names[-1]).lower())

    #build required account info
    first_name = str(names[0])
    last_name = str(names[-1])
    username = netlink_id
    email = netlink_id + '@uvic.ca'
    password = str(DEFAULT_PROF_ACCOUNT_PASSWORD)

    return (first_name, last_name, username, password, email)


def get_preferences_record_fields(csv_row):
    day_index_map = {
        0 : 'monday',
        1 : 'tuesday',
        2 : 'wednesday',
        3 : 'thursday',
        4 : 'friday'
    }
    semester_map = {
        'FALL': "fall",
        'SPRING': "spring",
        'SUMMER': "summer"
    }

    teaching_obligations = int(csv_row[PROF_CSV_COLUMNS.TEACHING_OBLIGATIONS.value])

    #parse preferred times per semester
    fall_dict = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": []
    }
    spring_dict = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": []
    }
    summer_dict = {
        "monday": [],
        "tuesday": [],
        "wednesday": [],
        "thursday": [],
        "friday": []
    }

    #splitting time strings for each day
    #fall
    for day_index in range(0, 5):
        day_times = str(csv_row[PROF_CSV_COLUMNS.FALL_PREFERRED_TIMES_MONDAY.value + day_index]).split('&')
        for timerange in day_times:
            start_time, end_time = timerange.split('~')
            fall_dict[day_index_map[day_index]].append([start_time, end_time])

    #spring
    for day_index in range(0, 5):
        day_times = str(csv_row[PROF_CSV_COLUMNS.SPRING_PREFERRED_TIMES_MONDAY.value + day_index]).split('&')
        for timerange in day_times:
            start_time, end_time = timerange.split('~')
            spring_dict[day_index_map[day_index]].append([start_time, end_time])

    #summer
    for day_index in range(0, 5):
        day_times = str(csv_row[PROF_CSV_COLUMNS.SUMMER_PREFERRED_TIMES_MONDAY.value + day_index]).split('&')
        for timerange in day_times:
            start_time, end_time = timerange.split('~')
            summer_dict[day_index_map[day_index]].append([start_time, end_time])

    #build full preferred times JSON field
    preferred_times = {
        "fall": fall_dict,
        "spring": spring_dict,
        "summer": summer_dict
    }

    #build preferred number of courses per sem
    preferred_courses_per_semester = {
        "fall": int(csv_row[PROF_CSV_COLUMNS.FALL_NUM_PREFERRED_COURSES.value]),
        "spring": int(csv_row[PROF_CSV_COLUMNS.SPRING_NUM_PREFERRED_COURSES.value]),
        "summer": int(csv_row[PROF_CSV_COLUMNS.SUMMER_NUM_PREFERRED_COURSES.value])
    }

    #build preferred nonteaching sem
    preferred_courses_per_semester = semester_map[csv_row[PROF_CSV_COLUMNS.PREFERRED_NON_TEACHING_SEMESTER.value]]

    #build preferred course day spreads
    preferred_course_day_spreads = str(csv_row[PROF_CSV_COLUMNS.PREFERRED_COURSE_DAY_SPREADS.value + day_index]).split('&')

    #TODO: figure out the following Preferences fields: taking_sabbatical, sabbatical_length, sabbatical_start_month, courses_preferences
    #
    #return [list of all Preferences fields]



# Converts the input Professors-object-related data (Profs info + Preferences info) CSV into Django model instances stored in the DB.
# Queries are performed to the DB to create objects & associate them with the correct relationships to other models.
def parse_professors_data(csv_file):
    with open(csv_file) as schedules_data_csv:
        csv_reader = csv.reader(schedules_data_csv, delimiter=',')

        #skip the header rows
        next(csv_reader)
        next(csv_reader)

        #get CSV data into memory (list of rows)
        csv_list = []
        for row in csv_reader:
            csv_row = list(row)
            print(csv_row)
            csv_list.append(csv_row)

        #Step 1 - build User objects then AppUser objects, which auto signal to create associated Preference
        for row in csv_list:
            if row[PROF_CSV_COLUMNS.ID.value]:
                #make username + password + email from fullname
                first_name, last_name, username, password, email = generate_account_fields(row[PROF_CSV_COLUMNS.FULL_NAME.value])
                user_attributes = {
                    'username': username,
                    'password': password,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_superuser': False
                }
                user = User.objects.create_user(**user_attributes)
                appuser_attributes = {
                    'user': user,
                    'prof_type': FACULTY_TYPE_MAP[row[PROF_CSV_COLUMNS.FACULTY_TYPE.value]],
                    'is_peng': BOOLEAN_MAP[row[PROF_CSV_COLUMNS.IS_PENG.value]],
                    'is_form_submitted': False
                }
                appuser = AppUser.objects.get_or_create(**appuser_attributes)

                #fetch the new empty Preferences record
                preferences_record = Preferences.objects.get(professor=appuser)

                #build Preferences record fields from the CSV row
                get_preferences_record_fields(row)

                preferences_fields = {
                    "professor": appuser,
                    "is_submitted": False,
                    "taking_sabbatical": True,
                    "sabbatical_length": "FULL",
                    "sabbatical_start_month": 1,
                    "preferred_times": {
                        "fall": [
                            {"day": 1, "time": 8},
                            {"day": 1, "time": 9}
                        ],
                        "spring": [
                            {"day": 3, "time": 8},
                            {"day": 3 ,"time": 9},
                        ],
                        "summer": [
                            {"day": 4, "time": 12},
                        ]
                    },
                    "courses_preferences": {
                            "CSC 225": {
                                "willingness": 1,
                                "difficulty": 1
                            },
                            "CSC 226": {
                                "willingness": 2,
                                "difficulty": 2
                            }
                    },
                    "preferred_non_teaching_semester": "fall",
                    "preferred_courses_per_semester": {
                            "fall": "1",
                            "spring": "2",
                            "summer": "3"
                        },
                    "preferred_course_day_spreads": [
                            "TWF",
                            "Th"
                        ],
                }



    return


def main():
    # Convert the schedule data CSV into Django model instances stored in the DB
    parse_schedules_data(SCHEDULES_CSV_FILE)

    # Convert the professors data CSV into Django model instances stored in the DB
    # parse_professors_data(PROFESSORS_CSV_FILE)

    #TODO: Probably add parsing methods for the other required data (Historical data + Enrolment data)
    return


if __name__ == '__main__':
    main()
    