# back-end

Company 2's back-end system

# Running the application

This is a Django application, where where Scheduler is considered the main project. It is broken up into 4 apps:
* Users
* Courses
* Preferences
* Schedule

This application uses Django 4.0, which requires Python >=3.8. This application uses PostgreSQL; to run migrations, see [Database Migrations](#database-migrations). 

## Docker

To run the application, first make sure you have [docker](https://docs.docker.com/desktop/) and [docker compose](https://docs.docker.com/compose/install/) installed.

To build and run the application, from the root directory run:
```
docker-compose up --build   //Add -d flag to run the containers in the background (detached mode)
```

Now in a separate terminal, apply any missing migrations using the command. The scheduler_service will say `You have # unapplied migration(s)` when starting the docker container if you are missing them.
```
docker-compose run web python manage.py migrate

```

Then go to [http://localhost:8000/](http://localhost:8000/) to see the Django app up and running. 

To stop the docker containers either use `ctrl c` if not running in detached mode or use the command
```
docker-compose down
```

When developing the app, if you add or modify models, you will have to apply them to the database. See the [Database Migrations](#database-migrations) sections for more information. 

## Testing

To test the application, ensure that the app is running with [docker](Docker). Then open up a new terminal. 

Then within the root folder, run the command

```
docker-compose run web python manage.py test
```

It will run the tests and notify you of any failures.

To run a specific app's test cases, use the command

```
docker-compose run web python manage.py test <app_name>
```

# Development

Since the app has been containerized, any changes that you make will be picked up by docker as long as the app is running. 

## Database Migrations

When developing, if you create or modify models you need to apply them to the database.

First you need to tell Django that you made some changes to the models and you would like the changes to be stored as a migration.

To do this, ensure that the application and db are running in [docker](Docker) and in a terminal use the following command:

```
docker-compose run web python manage.py makemigrations
```

Now create those model tables in the database:

```
docker-compose run web python manage.py migrate
```

This will take all the migrations that haven't been applied and runs them against your db.

## Useful Links

This initial repo was created using the following links:

[Django Rest Framework Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)

[Django App Tutorial](https://docs.djangoproject.com/en/4.0/intro/tutorial01/)

[Building an API Django REST Framework](https://medium.com/backticks-tildes/lets-build-an-api-with-django-rest-framework-32fcf40231e5)

[Docker Compose Django](https://docs.docker.com/samples/django/)
