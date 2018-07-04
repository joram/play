# play
`"where I go to do battlesnake" ~Brad`

This is the module that users of all types use to interact with the game engine and other pieces.


## Setup

### On Mac
- install brew https://brew.sh/
- clone the repo: `git clone git@github.com:battlesnakeio:play`
- install python3: `brew install python3`
- install libraries: `pip3 install -r requirements.txt`
- go into play folder: `cd play`
- migrate: `django-admin migrate`
- start the server: `django-admin runserver`
- setup databases
- visit the app att `localhost:8000`

### On Linux
- clone the repo: `git clone git@github.com:battlesnakeio:play`
- install python3: `apt-get install python3`
- install libraries: `pip install -r requirements.txt`
- go into the play folder `cd play`
- migrate: `django-admin migrate`
- start the server: `django-admin runserver`
- setup databases
- visit the app att `localhost:8000`


### Github OAuth
Go here: `https://github.com/settings/applications`

Filling in the following:
- URL = `http://localhost:8000`
- Callback = `http://localhost:8000/oauth/complete/github`

Copy the generated secrets in  to `/.env` (described below)


### Secrets
you're `/.env` file should look like:
```bash
BATTLESNAKEIO_SECRET=battlesnakeio
BATTLESNAKEIO_GITHUB_CLIENT_ID=...
BATTLESNAKEIO_GITHUB_CLIENT_SECRET=...
BATTLESNAKEIO_POSTGRES_HOST=...
POSTGRES_DB=battlesnakeio_play
POSTGRES_USER=battlensakeio
POSTGRES_PASSWORD=battlesnakeio
```
*NOTE:* probably best to change from defaults


### Docker
- build the image
`docker build -t battlesnakeio/play .`
- run database
`docker run -it -d --env-file=.env -p 5432:5432 --name=battlesnakeio.play.pg postgres:10.4`
- run server
`docker run -it -d --env-file=.env -p 8000:8000 --name=battlesnakeio.play battlesnakeio/play`
