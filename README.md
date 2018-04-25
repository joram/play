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

### Github OAuth
Go here: `https://github.com/settings/applications`

Filling in the following:
- URL = `http://localhost:8000`
- Callback = `http://localhost:8000/oauth/complete/github`

Set the generated secrets in environment variables:
```bash
GITHUB_CLIENT_ID=...
GITHUB_CLIENT_SECRET=...
```