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
## 🚀 Installation

### 🐳 Run the App in a Docker Container

1. **Clone the repository**  
   ```sh
   git clone -b dev git@github.com:4ikkamony/planetarium-api.git
   ```  
   ```sh
   cd planetarium-api
   ```  

3. **Set up environment variables**  
   ```sh
   mv docker/.env.sample docker/.env
   ```  

   - Fill in your [Stripe API Keys](https://support.stripe.com/questions/what-are-stripe-api-keys-and-how-to-find-them):  
     - STRIPE_PUBLISHABLE_KEY  
     - STRIPE_SECRET_KEY  
   - The rest can be left as default for local development.  

4. **Start the containers**  
   ```sh
   docker compose -f docker/docker-compose.yaml up  
   ```
5. **Run tests (while the container is running)**  
   ```sh
   docker exec -it planetarium-backend pytest  
   ```
---

### 💻 Run Locally with a Database Container

The steps are almost the same, except you'll be running the backend locally while using the database inside Docker.

1. **Clone the repository**  
   ```sh
   git clone -b dev git@github.com:4ikkamony/planetarium-api.git  
   ```
   ```sh
   cd planetarium-api  
   ```

2. **Set up environment variables**  
   ```sh
   mv docker/.env.sample docker/.env  
   ```
   - Fill in your [Stripe API Keys](https://support.stripe.com/questions/what-are-stripe-api-keys-and-how-to-find-them).  
   - Set POSTGRES_HOST=localhost to connect to the database container.  

3. **Start only the database container**  
   ```sh
   docker compose -f docker/docker-compose-local.yaml up  
   ```
4. **Navigate to the source directory**  
   ```sh
   cd src  
   ```
   
5. **Apply migrations, load initial data, and run the server**  
   ```sh
   python manage.py makemigrations && \  
   python manage.py migrate && \  
   python manage.py loaddata data/planetarium_db_data.json && \  
   python manage.py runserver  
   ```

6. **Run tests(when in src/)**   
   ```sh
   pytest
   ```  

---

## 📖 After Installation  
Visit Swagger API Docs at http://127.0.0.1:8000/api/doc/swagger/ to see available endpoints and some example requests.
