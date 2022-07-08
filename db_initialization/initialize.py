import csv
import pprint
import json
import os

#CSV files containing relevant to be parsed
SCHEDULES_CSV_FILE = '' #TODO
PROFESSORS_CSV_FILE = '' #TODO
HISTORICAL_CAPACITIES_CSV_FILE = '' #TODO



# Converts the input Schedule-object-related data (Courses +++) CSV into Django model instances stored in the DB.
# Queries are performed to the DB to create objects & associate them with the correct relationships to other models.
def parse_schedules_data(csv_file):
    #TODO...

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
    