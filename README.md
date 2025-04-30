# BNPL Backend

This repository contains the backend for the BNPL application, built with Django.
Follow these steps to set up and run the application in a development environment.

## Prerequisites

Make sure you have the following installed:

- Python 3.11+
- Docker & Docker Compose (optional)
- PostgreSQL or SQLite (based on project setup)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/zilehuda/bnpl-backend.git
cd bnpl-backend
```

### Install Dependencies

Set up and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
configure pre-commit (you must have git) (optional)

```bash
$ pre-commit install
```

Then, install the required packages:
```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Copy the .env.example file to .env
```bash
cp .env.example .env
```

Open the .env file and configure your environment variables as needed.

### Start PostgreSQL Database with Docker Compose

To run a PostgreSQL database in Docker, use the provided docker-compose.dev.yml file:

```bash
docker-compose -f docker-compose.dev.yml up db -d
```

This will set up the PostgreSQL container with the following connection details:
`
PostgreSQL URL: postgresql://admin:admin@localhost:5432/bnpl_db`

Make sure these credentials match the settings in your `.env` file.


### Run celery & celery beat (mac)
To run celery
```
celery -A core worker --loglevel=info -c 4
```

To run celery-beat
```
celery -A core beat -l info -S django
```

### Run Database Migrations

Apply the database migrations to set up the database schema:

```bash
python manage.py migrate
```

### Run the Application

Finally, start the Django development server:

```bash
python manage.py runserver
```

Your application will be available at http://127.0.0.1:8000/.


## Trade-offs and Known Limitations

I simplified date validation for invoice due dates to avoid timezone handling complexity. Consider improving this before production use.

The app assumes a single currency (USD) for all transactions.

Form validation is basic and may require enhancement for edge cases.

Frontend state management is minimal and may become hard to maintain as the app grows.
