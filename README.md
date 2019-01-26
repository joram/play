# play

> "Where I go to do battlesnake." - @bvanvugt

This is the platform that allows users to sign up, register snakes, and run games.

## Getting Started

### Prerequisites

- On a mac? If you haven't already, install [brew](https://brew.sh/)
- A [Github OAuth App](#github-oauth-app-configuration)
- Postgres 10.4

### Setup

1. Clone the repo to your machine: `git clone git@github.com:battlesnakeio:play`
1. Install python3.x
    - on a Mac: `brew install python3`
      - Alternatively, use [`pyenv`](https://github.com/pyenv/pyenv) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv) to manage your python installations
    - on Linux: `apt-get install python3`
1. Install the project dependencies:
    ```shell
    pip3 install -r requirements.txt
    ```
    - Using pyenv? Use `pip` supplied by your virtualenv instead of `pip3`
    - optionally install via pyenv
        ```
        pyenv install 3.7
        pyenv virtualenv 3.7 play
        pyenv activate play
        ```

1. From inside the project `play` folder, run the migrations:
    ```shell
    ENV=local \
    PYTHONPATH=~/path/to/play/play \
    ./manage.py migrate
    ```
1. Start the server with:
    ```shell
    ENV=local \
    PYTHONPATH=~/path/to/play/play \
    ./manage.py runserver
    ```
1. Visit the app running at <http://localhost:8000>


### Tests

To run tests:

```shell
cd play
ENV=local pytest
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
ENV=local

BATTLESNAKEIO_SECRET=battlesnakeio
BATTLESNAKEIO_GITHUB_CLIENT_ID=...
BATTLESNAKEIO_GITHUB_CLIENT_SECRET=...
```

If using postgres locally (instead of SQLite), you'll also need:

```bash
POSTGRES_HOST=...
POSTGRES_PORT=...
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
```

## Docker

Docker is used to build the production image that gets deployed. You can also use it to build an image you can run yourself:

1. Build the image: `docker build -t battlesnakeio/play .`
2. Run databases: `docker run -it -d --env-file=.env -p 5432:5432 --name=battlesnakeio.play.pg postgres:10.4`
3. Run server: `docker run -it -d --env-file=.env -p 8000:8000 --name=battlesnakeio.play battlesnakeio/play`
