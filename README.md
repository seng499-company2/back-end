# back-end
Company 2's back-end system

# Running the application
This is a Django application, where where Scheduler is considered the main project. 
hello_world is an example Django application within Scheduler that needs to be removed later. 

This application uses Django 4.0, which requires Python >=3.8.

Please note that this was created using the basic setup that defaults to Sqlite, therefore it will need to be removed later on when a database is selected.

## Locally
When running it locally, it is first recommended to create a virtual environment. 
If you haven't done so, please see [Virtual Environment](#venv) section.

To run it local use the command 
```
python manage.py runserver
```
Then go to [http://localhost:8000/api/v1/world/](http://localhost:8000/api/v1/world/) to hit an API endpoint. If successfully running, it should return three worlds.  

Use Ctrl C to stop.

## Docker
To run the application, first make sure you have [docker](https://docs.docker.com/desktop/) and [docker compose](https://docs.docker.com/compose/install/) installed. 

To build and run the application, from the root directory run
```
docker-compose up
```

Then again go to the above url to hit the endpoint and use Ctrl C to stop.

## Testing
To test the application, first ensure there are tests within the corresponding app. See hello_world.test for an example.
Then within the root folder, run the command
```
python manage.py test
```
It will run the tests and notify you of any failures. 

# Development
Here are some development tips and tricks. 

## <a name="venv"></a> Virtual Environment 
To help isolate dependencies, it is recommended to first create a virtual environment before running the application.

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

## Database Migrations
When developing, if you create any new models you need to add them to the database. 

First you need to tell django that you made some changes to the models and you would like the changes to be stored as a migration. 
To do this run: 
```
 python manage.py makemigrations <app_name>
```
Now create those model tables in the database:
```
python manage.py migrate
```
This will take all the migrations that haven't been applied and runs them against your db. 


## Useful Links
This initial repo was created using the following links:

[Django Rest Framework Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)

[Django App Tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/)

[Building an API Django REST Framework](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5)

[Docker Compose Django](https://docs.docker.com/samples/django/)