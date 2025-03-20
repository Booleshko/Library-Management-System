# Library-Management-System
API service for borrowing a book.

****

## Installing using GitHub

**Install PostgresSQL and create db**
- git clone https://github.com/Booleshko/Library-Management-System.git
- cd DRF Library Practice
- python -m venv venv
- source venv/bin/activate
- pip install requirements.txt
- SECRET_KEY = your secret key
- DB_PASSWORD = your password
- DB_USER = your db username
- DB_NAME = your db name
- DB_HOST= your db hostname
- python manage.py migrate
- python manage.py runserver

****

## Running API with docker
**Docker should be installed, and db properly configured. (see above)**

- docker-compose build
- docker-compose up
- Create admin user. First: "docker exec -it [container identifier hash] bash" then: "python manage.py createsuperuser"
- To run tests: python manage.py test. (You should be inside the container)

****

## Getting access
****Make sure ModHeader or any other browser extension for authentication is installed. Use Authorize as a header****

- create user via api/user/register
- get access token via api/user/token

## Features

- JWT authentication
- Admin panel /admin/
- API documentation is at /api/doc/swagger/
- Create/Update/Delete for books endpoints (Admin only)
- Create/Delete borrowing for particular book (Users, Admin)
- Book endpoint only available for view for authenticated/unauthenticated users
