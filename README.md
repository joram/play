# play
`"where I go to do battlesnake" ~Brad`

This is the module that users of all types use to interact with the game engine and other pieces.

## Setup
### On Linux
- install python3: `apt-get install python3`
- install libraries: `pip install -r requirements.txt`
- migrate: `django-admin migrate`
- start the server: `django-admin runserver`
- setup databases
- visit the app att `localhost:8000`

### Libraries
Using the latest python/django
```
Python 3.6.3
Django 2.0.3
```

## Docker Stuff
```
docker build . -t triptracks
docker tag triptracks us.gcr.io/tripplanner-1488762973379/triptracks:latest
```

