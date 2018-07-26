# play

`"where I go to do battlesnake" ~Brad`

This is the module that users of all types use to interact with the [game engine](https://github.com/battlesnakeio/engine) and other pieces.

## Getting Started

### Prerequisites

- On a mac? If you haven't already, install [brew](https://brew.sh/)
- A [Github OAuth App](#github-oauth-app-configuration)

### Setup

1. Clone the repo to your machine: `git clone git@github.com:battlesnakeio:play`
2. Install python3.x
    - on a Mac: `brew install python3`
      - Alternatively, use [`pyenv`](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv) to manage your python installations
    - on Linux: `apt-get install python3`
3. Install the project dependencies:
    ```shell
    pip3 install -r requirements.txt
    ```
    - Using pyenv? Use `pip` supplied by your virtualenv instead of `pip3`
4. From inside the project `play` folder, run the migrations: `django-admin migrate`
5. Start the server with:
    ```shell
    ENV=local \
    PYTHONPATH=~/path/to/play/play \
    ./manage.py runserver
    ```
6. Setup databases
7. Visit the app running at <http://localhost:8000>

### Tests

To run tests:

```shell
cd play
pytest
```

### Github OAuth App Configuration

Go here: <https://github.com/settings/applications/new>

Fill in the following:

- Name = whatever you want
- URL = <http://localhost:8000>
- Callback = <http://localhost:8000/oauth/complete/github>

Copy the generated secrets in to your `.env` (described below)

### Secrets

Your `.env` file should contain the following:

```bash
BATTLESNAKEIO_SECRET=battlesnakeio
BATTLESNAKEIO_GITHUB_CLIENT_ID=...
BATTLESNAKEIO_GITHUB_CLIENT_SECRET=...
BATTLESNAKEIO_POSTGRES_HOST=...
POSTGRES_DB=battlesnakeio_play
POSTGRES_USER=battlensakeio
POSTGRES_PASSWORD=battlesnakeio
```

*NOTE:* Don't use the defaults, it is highly encouraged you customize these values

## Docker

Docker is used to build the production image that gets deployed. You can also use it to build an image you can run yourself:

1. Build the image: `docker build -t battlesnakeio/play .`
2. Run databases: `docker run -it -d --env-file=.env -p 5432:5432 --name=battlesnakeio.play.pg postgres:10.4`
3. Run server: `docker run -it -d --env-file=.env -p 8000:8000 --name=battlesnakeio.play battlesnakeio/play`
