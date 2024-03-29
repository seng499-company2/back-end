from rest_framework.views import APIView
from django.http import HttpResponse
from django.http import HttpRequest
from rest_framework import status

from coursescheduler import generate_schedule as c2alg1# Company 2 alg 1 
from forecaster.forecaster import forecast as c2alg2 # company 2 alg 2

from c1algo1 import scheduler as c1alg1# company 1 alg 1
from c1algo2.forecaster import forecast as c1alg2

from schedule.alg_data_generator import get_historic_course_data, get_schedule, get_program_enrollment_data, \
    get_professor_dict, get_profs_error, get_schedule_error

import traceback
import json
import logging
import pickle

debugging = False

class Schedule(APIView):
    # GET / schedule / {year - semester}
    def get(self, request: HttpRequest, year: int, semester: str, requested_company_alg: int) -> HttpResponse:
        print("received GET request to Schedule API Endpoint")

        # Create params for algorithms packages
        historical_data = get_historic_course_data()
        previous_enrollment = get_program_enrollment_data()
        try:
            schedule = get_schedule(requested_company_alg)
        except FileNotFoundError as e:
            return HttpResponse("Error generating schedule! Did you initialize the database?",
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        professors = get_professor_dict()

        # GET / schedule / {year - semester}/?use_mock_data=true
        if "use_mock_data" in request.query_params and request.query_params["use_mock_data"] == 'true':
            professors = get_profs_error()
            schedule = get_schedule_error()

        try:
            alg_2_output = c1alg2(historical_data, previous_enrollment, schedule) if requested_company_alg == 1 \
                 else c2alg2(historical_data, previous_enrollment, schedule, 2, logging.INFO)
            if requested_company_alg == 1:
                if debugging:
                    profs_pickle = open('profs_c1.pickle', 'wb')
                    pickle.dump(professors, profs_pickle)
                    profs_pickle.close()
                    schedule_pickle = open('schedule_c1.pickle', 'wb')
                    pickle.dump(alg_2_output, schedule_pickle)
                    schedule_pickle.close()
                schedule, error = c1alg1.generate_schedule(professors, alg_2_output)
            else:
                if debugging:
                    profs_pickle = open('profs_c2.pickle', 'wb')
                    pickle.dump(professors, profs_pickle)
                    profs_pickle.close()
                    schedule_pickle = open('schedule_c2.pickle', 'wb')
                    pickle.dump(alg_2_output, schedule_pickle)
                    schedule_pickle.close()
                #print Alg2 output to file
                with open('input_sched.json', 'w') as f:
                    f.write(json.dumps(alg_2_output))

                with open('input_profs.json', 'w') as f:
                    f.write(json.dumps(professors))

                schedule, error = c2alg1(professors, alg_2_output, False)
            if error is not None and error != "":
                return HttpResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return HttpResponse(json.dumps(schedule), status=status.HTTP_200_OK)
        except Exception as err:
            print(traceback.format_exception(err))
            return HttpResponse("ERROR WITH ALGORITHMS", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST / schedule / {scheduleId} / {courseId}
    def post(self, request: HttpRequest, schedule_id: str, course_id: str,  company_alg: int) -> HttpResponse:
        print("received POST request to Schedule API Endpoint")
        body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)


class ScheduleFile(APIView):
    # GET / schedules / files / {scheduleId}
    def get(self, request: HttpRequest, schedule_id: str,  company_alg: int) -> HttpResponse:
        print("received GET request to ScheduleFile API Endpoint")
        body = "GENERATED SCHEDULE FROM COMPANY %d ALGORITHM" % company_alg
        return HttpResponse(body, status=status.HTTP_200_OK)
