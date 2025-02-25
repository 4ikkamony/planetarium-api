# PplAnetAVLO: To the Stars and Beyond

![Django](https://img.shields.io/badge/Django-5.1-blue?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django)
![pytest](https://img.shields.io/badge/pytest-8.3-blue?logo=pytest)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=PostgreSQL&logoColor=blue)
![Swagger](https://img.shields.io/badge/Swagger-UI-lightgreen?logo=swagger)
![Docker](https://img.shields.io/badge/Docker-28.0-blue?logo=docker)
![Stripe](https://img.shields.io/badge/Stripe-API-violet?logo=stripe)

This is the **Planetarium Management API**, built with Django and Django REST Framework.

---

## Features

- Manage shows, bookings, and events in a planetarium
- Swagger Documentation
- JWT Authentication
- PostgreSQL full-text and trinagam similarity search for Shows
- Stripe Checkout Sessions for payments
- Fully containerized with Docker

---

## Installation

## Run app in Docker container:

```sh
git clone -b dev git@github.com:4ikkamony/planetarium-api.git
```

```sh
cd planetarium-api
```

```sh
mv docker/.env.sample docker/.env
```

Fill in [Stripe API Keys:](https://support.stripe.com/questions/what-are-stripe-api-keys-and-how-to-find-them) STRIPE_PUBLISHABLE_KEY and STRIPE_SECRET_KEY

The rest of the values may be left as default, since we're running locally

```sh
docker compose -f docker/docker-compose.yaml up
```

To run tests when container is running:
```sh
docker exec -it planetarium-backend pytest
```

## Run app localy with DB cointainer

The steps almost the same:

```sh
git clone -b dev git@github.com:4ikkamony/planetarium-api.git
```

```sh
cd planetarium-api
```

```sh
mv docker/.env.sample docker/.env
```

Fill in [Stripe API Keys:](https://support.stripe.com/questions/what-are-stripe-api-keys-and-how-to-find-them) STRIPE_PUBLISHABLE_KEY and STRIPE_SECRET_KEY

Set POSTGRES_HOST=localhost

```sh
docker compose -f docker/docker-compose-local.yaml up
```
```sh
cd src
```

```sh
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py loaddata data/planetarium_db_data.json && \
python manage.py runserver
```

To run tests, when in src/ run:
```sh
pytest
```
# After installation
## Visit http://127.0.0.1:8000/api/doc/swagger/ to see available endpoints(and some examples)
