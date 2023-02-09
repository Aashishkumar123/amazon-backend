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
$ python3 manage.py migrate
```
## Run the project
<em>To run the project is very simple just hit this command</em>
```console
$ python3 manage.py runserver
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
