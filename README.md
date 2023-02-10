# Amazon Clone API
<em>Amazon clone api using django and django rest framework.</em>

## Requirements

Python 3.6+

## Installation

```console
$ pip install -r requirements.txt
```
## Database setting
<em>Go to settings.py file and change the database settings.</em>
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your-database-name',
        'USER': 'Your-username',
        'PASSWORD': 'Your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
<em>and then hit the migrate command to successfully create database table..</em>

```console
$ python manage.py migrate
```
## Run the project
<em>To run the project is very simple just hit this command</em>
```console
$ python manage.py runserver
```

## API Documentations
<em>If you want api documentations simple visit this</em>

<b>swagger docs</b>
```console
$ http://localhost:8000/api/amz/swagger/
```
<b>ReDocs docs</b>
```console
$ http://localhost:8000/api/amz/redoc/
```
## Testing
<em>If you want to run the test cases you can simply run this command</em>
```console
$ python manage.py test
```
<em>Hence all api testing code are wriiten in test.py file.</em>

## Code Format
<em>If you want to format the code you can simply run those commands.</em>
<br /> <br />
<b>using black package</b>
```console
$ black amazon_backend_api/api/views.py
```
<b>using flake8 package</b>
```console
$ flake8 amazon_backend_api/api/views.py
```

## Postman api collection
<em>You can also export the <a href="https://github.com/Aashishkumar123/amazon-backend/blob/master/AMAZON%20API.postman_collection.json">postman api collection</a> and import in postman.</em>

## Run server through Docker
<em>If you want to run the server using docker-compose hit the following command.</em>

```docker
$ docker-compose up --build
```
