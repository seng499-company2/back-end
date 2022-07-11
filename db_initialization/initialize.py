import csv
import pprint
import json
import os
from enum import Enum

from schedule.Schedule_models import A_Schedule, A_TimeSlot, A_CourseSection, A_Course, A_CourseOffering

#CSV files containing relevant to be parsed
SCHEDULES_CSV_FILE = '' #TODO
PROFESSORS_CSV_FILE = '' #TODO
HISTORICAL_CAPACITIES_CSV_FILE = '' #TODO


#maps CSV boolean types to Python T/F
BOOLEAN_MAP = {
    'TRUE': True,
    'False': False,
    '': None
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
        line_count = 0

        #get CSV data into memory (list of rows)
        csv_list = []
        for row in csv_reader:
            csv_row = list(row)
            csv_list.append(csv_row)

        #Step 1 - build TimeSlot objects
        for row in csv_list:
            #handling TimeSlots for course with 1 section
            if row[CSV_COLUMNS.SECTION1_TIME_RANGE]:
                
                #parse the DaysOfTheWeek CSV string into distinct enum values + TimeRange splittings
                days_list = get_days_of_the_week(row[CSV_COLUMNS.SECTION1_DAYS_OF_WEEK])
                time_range = str(row[CSV_COLUMNS.SECTION1_TIME_RANGE]).split('~')

                #create Django models & store to DB
                for day in days_list:
                    _, _ = A_TimeSlot.objects.get_or_create(
                        dayOfWeek=day,
                        timeRange=time_range
                    )

            #extra case - handling TimeSlots for course with 2 sections
            if row[CSV_COLUMNS.NUM_SECTIONS] == 2:
                if row[CSV_COLUMNS.SECTION2_TIME_RANGE]:
                    
                    #parse the DaysOfTheWeek CSV string into distinct enum values + TimeRange splittings
                    days_list = get_days_of_the_week(row[CSV_COLUMNS.SECTION2_DAYS_OF_WEEK])
                    time_range = str(row[CSV_COLUMNS.SECTION2_TIME_RANGE]).split('~')

                    #create Django models & store to DB
                    for day in days_list:
                        _, _ = A_TimeSlot.objects.get_or_create(
                            dayOfWeek=day,
                            timeRange=time_range
                        )


        #Step 2 - build Course objects
        for row in csv_list:
            course_code = row[CSV_COLUMNS.CODE]
            title = row[CSV_COLUMNS.TITLE]
            peng_required = {
                "fall": BOOLEAN_MAP[row[CSV_COLUMNS.PENG_REQUIRED_FALL]],
                "spring": BOOLEAN_MAP[row[CSV_COLUMNS.PENG_REQUIRED_SPRING]],
                "summer": BOOLEAN_MAP[row[CSV_COLUMNS.PENG_REQUIRED_SUMMER]]
            }
            year_required = int(row[CSV_COLUMNS.YEAR_REQUIRED])

            #create Django models & store to DB
            _, _ = A_Course.objects.get_or_create(
                code=course_code,
                title=title,
                pengRequired=peng_required,
                yearRequired=year_required
            )

            
        #Step 3 - build CourseSection objects *(For Static courses only)*
        for row in csv_list:                
            if row[CSV_COLUMNS.SECTION1_PROF_ID]:
                professor = {
                    "id" : row[CSV_COLUMNS.SECTION1_PROF_ID] ,
                    "name" : row[CSV_COLUMNS.SECTION1_PROF_NAME]
                }
            else:
                professor = None
            
            if row[CSV_COLUMNS.SECTION1_CAPACITY]:
                capacity = int(row[CSV_COLUMNS.SECTION1_CAPACITY])
            else:
                capacity = 0

            #create Django models & store to DB
            courseSection1, created = A_CourseSection.objects.get_or_create(
                professor=professor,
                capacity=capacity
            )
            
            #Section 2 prof id
            if row[CSV_COLUMNS.NUM_SECTIONS] == 2:
                if row[CSV_COLUMNS.SECTION2_PROF_ID]:
                    professor = {
                        "id" : row[CSV_COLUMNS.SECTION2_PROF_ID] ,
                        "name" : row[CSV_COLUMNS.SECTION2_PROF_NAME]
                    }
                else:
                    professor = None
                
                if row[CSV_COLUMNS.SECTION2_CAPACITY]:
                    capacity = int(row[CSV_COLUMNS.SECTION2_CAPACITY])
                else:
                    capacity = 0

                #create Django models & store to DB
                courseSection2, created = A_CourseSection.objects.get_or_create(
                    professor=professor,
                    capacity=capacity
                )

            #create the TimeSlots many-to-many relationship, if exists
            if row[CSV_COLUMNS.SECTION1_DAYS_OF_WEEK] and :
                days_list = get_days_of_the_week(row[CSV_COLUMNS.DAYS_OF_WEEK])
                time_range = str(row[CSV_COLUMNS.TIME_RANGE]).split('~')
                time_slots = []
                for day in days_list:
                    #get TimeSlot obj
                    obj, _ = A_TimeSlot.objects.get_or_create(
                        dayOfWeek=day,
                        timeRange=time_range
                    )

                    #associate the TimeSlot
                    time_slots.append(obj)

                courseSection.timeSlots.set(time_slots)

                #
        
        #Step 4 - build CourseOffering objects
        """
        #one instance of this class should represent a single Course & CourseSection pair
        '''PRIMARY KEY: id (Django auto)'''
        class A_CourseOffering(models.Model):
            course = models.ForeignKey(A_Course, related_name='courseOfferings', blank=True, null=True, on_delete=models.CASCADE)    #One-to-Many: course to courseOfferings
            sections = models.ManyToManyField(A_CourseSection, related_name='courseOfferings')

            def __str__(self):
                return 'id: ' + str(self.id) + ', ' + str(self.course.code) + ', Number of Sections: ' + str(len(self.sections.all()))
        """
        for row in csv_list:
            #get associated Course object foreign key to create CourseOffering, then save to DB
            course_code = row[CSV_COLUMNS.CODE]
            obj = A_Course.objects.get(code=course_code)

            if obj is not None:
                courseOffering = A_CourseOffering.objects.create(course=obj)

                #get the associated CourseSection for a many-to-many relationship, if a section exists (static courses only)
                days_list = get_days_of_the_week(row[CSV_COLUMNS.DAYS_OF_WEEK])
                time_range = str(row[CSV_COLUMNS.TIME_RANGE]).split('~')
                time_slots = []
                for day in days_list:
                    #get TimeSlot obj
                    obj, _ = A_TimeSlot.objects.get_or_create(
                        dayOfWeek=day,
                        timeRange=time_range
                    )
                    time_slots.append(obj)

                section = A_CourseSection.objects.get(professor=professor, capacity=capacity, timeSlots=time_slots)
                
                #TODO: must fix the above logic ^ and update all previous work to work with updated Schedule.csv



    return


# Converts the input Professors-object-related data (Profs info + Preferences info) CSV into Django model instances stored in the DB.
# Queries are performed to the DB to create objects & associate them with the correct relationships to other models.
def parse_professors_data(csv_file):
    #TODO...

    return


def main():
    # Convert the schedule data CSV into Django model instances stored in the DB
    parse_schedules_data(SCHEDULES_CSV_FILE)

    # Convert the professors data CSV into Django model instances stored in the DB
    parse_professors_data(PROFESSORS_CSV_FILE)

    #TODO: Probably add parsing methods for the other required data (Historical data + Enrolment data)
    return


if __name__ == '__main__':
    main()
    