
## Getting Started

Do you have  [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed? Here's the quick way to get started.

- Setup your `.env` file. 
- Build the containers: `docker-compose build`
- Start the containers: `docker-compose up`. This will follow logs from both the database + django. 
- Migrate your database (in a new terminal window): `docker-compose run play python3 manage.py migrate`.

Once the first time setup is complete, you can start development running `docker-compose up`. To exit, use `CTRL+C`. 
