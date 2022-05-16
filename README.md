# back-end
Company 2's back-end system

# Virtual Environment 
To help isolate dependecies, would recommend creating a virtual environment. 
To do this run:
```
# Create virtual env
python -m venv django_env

# Activate virtual env
source ./django_env/bin/activate
```
Once running the virtual env, install the dependencies once. 
```
pip install -r requirements.txt
```
In the future, make sure to activate this in order to run the application. 

To stop the virtual environment, just run `deactivate` in your terminal. 
# Running the application
The system is setup where Scheduler is considered the main project and contains the project's settings. 
While hello_world is an Django application within Scheduler. 
## Running Locally
To run it local use the command 
```
python manage.py runserver
```
Then go to http://localhost:8000/admin/ to see the admin page or http://localhost:8000/api/v1/world/ to hit an API endpoint. 

## Running on Docker
To run the application, first make sure you have docker installed. 

# Testing
To test the application, first ensure there are tests within the corresponding app. See hello_world.test for an example.
Then within the root folder, run the command
```
python manage.py test
```
It will run the test and notify you of any failures. 

# Useful Links
This initial repo was created using the following links:
(Django Rest Framework Quickstart)[https://www.django-rest-framework.org/tutorial/quickstart/]
(Building an API Django REST Framework)[https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5]
(Docker Compose Django)[https://docs.docker.com/samples/django/]