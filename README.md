Project Setup:
1. git clone the repository and go inside the directory
2. create and activate your virtual environment
   -run the following commands:
       -python -m venv env
       -venv\Scripts\activate #for Windows users
3. Required installations:
   -pip install django mysqlclient
   -pip install djangorestframework

Prerequisites:
-Python (version used: 3.11.9)
-MySQL (for the database)
-Django (web framework)
-Postman (for API testing)

MySQL setup:
-create database railway_db;

Configure the database setup:
-In the settings.py file, update the DATABASES settings to connect to your MySQL database.

Apply migrations to set up the database schema:
-python manage.py migrate

To run the application:
-run the following command to start the Django server:
    -python manage.py runserver
This will run the application on http://127.0.0.1:8000/
To access the app:
append http://127.0.0.1:8000/ with:
- api/ register/  --> for registering a user
- api/ login/  --> for user login
- api/ train/add/  --> to add new train details 
- api/ availability/<str:source>/<str:destination>/  --> to get seat availability
- api/ book/<int:train_id>/  --> to book a seat
- api/ booking/<int:booking_id>/  --> to get specific booking details
