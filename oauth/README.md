# Tusky's OAuth Server

## API Endpoints:
  - /o/authorize
  - /o/token
  - /o/revoke_token
  - /o/introspect

## Initial setup
<!-- Todo: Automate with Docker -->
  - Ensure [Poetry](https://python-poetry.org/) is installed
  - `poetry run python manage.py`
  - Create admin account at localhost:8000/admin/login
  - Create a Tusky web-app at localhost:8000/o/applications/register

<!-- Todo: Disable http -->
<!-- Todo: Ensure OAuth2_provider.urls can't be exploited -->

