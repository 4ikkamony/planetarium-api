# PplAnetAVLO: to the stars and beyond

This is planetarium management API, built wth DRF

# Features

# Installation

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

Visit http://127.0.0.1:8000/api/doc/swagger/ to see available endpoints

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
