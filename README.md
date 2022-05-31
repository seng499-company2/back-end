# back-end

Company 2's back-end system

# Running the application

This is a Django application, where where Scheduler is considered the main project.
hello_world is an example Django application within Scheduler that needs to be removed later.

This application uses Django 4.0, which requires Python >=3.8.

This application uses PostgreSQL; to run migrations, run `docker-compose exec web python manage.py migrate`

## Docker

To run the application, first make sure you have [docker](https://docs.docker.com/desktop/) and [docker compose](https://docs.docker.com/compose/install/) installed.

To build and run the application, from the root directory run

```
docker-compose up
```

Then go to [http://localhost:8000/api/v1/world/](http://localhost:8000/api/v1/world/) to hit an API endpoint

## Testing

To test the application, first ensure that the app is running see [docker](##Docker), and also make sure the are tests within the corresponding app and the app - see hello_world.test for an example.

Then within the root folder, run the command

```
python manage.py test
```

It will run the tests and notify you of any failures.

# Development

Since the app has been containerized, any changes that you make will be picked up by docker as long as the app is running

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
