# PplAnetAVLO: To the Stars and Beyond

![Python](https://img.shields.io/badge/Python-3.13.2-blue?logo=python&logoColor=yellow)
![Django](https://img.shields.io/badge/Django-5.1-blue?logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=django)
![pytest](https://img.shields.io/badge/pytest-8.3-blue?logo=pytest)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue?logo=PostgreSQL&logoColor=blue)
![Swagger](https://img.shields.io/badge/Swagger-UI-lightgreen?logo=swagger)
![Docker](https://img.shields.io/badge/Docker-28.0-blue?logo=docker)
![Stripe](https://img.shields.io/badge/Stripe-API-violet?logo=stripe)

This is the **Planetarium Management API**, built with Django and Django REST Framework.

---
# Contents
1. [Features](#features)
3. [Installation](#-installation)
   - [Run the App in a Docker Container](#-run-the-app-in-a-docker-container)
   - [Run the App Locally](#-run-locally-with-just-a-database-container)
5. [After Installation](#-after-installation)
   - [Usage Guide](#usage-guide)
---

## Features

- Manage shows, bookings, and events in a planetarium
- Swagger Documentation
- JWT Authentication
- PostgreSQL full-text and trinagam similarity search for Shows
- Stripe Checkout Sessions for payments
- Fully containerized with Docker

[⬆️](#contents)

---
## 🚀 Installation
   Make sure you have Python and Docker up and running

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
   - The rest can be left as default for local setup.
     Make sure POSTGRES_HOST set to 'db'(it's default postgres container name in this project)

4. **Start the containers**  
   **On Linux**
   ```sh
   nohup docker compose -f docker/docker-compose.yaml up &
   ```
   **On Windows**
   ```sh
   start docker compose -f docker/docker-compose.yaml up
   ```
5. **🧪 Run tests (while the container is running)**  
   ```sh
   docker exec -it planetarium-backend pytest  
   ```

[⬆️](#contents)

---

### 💻 Run Locally with just a Database Container

The steps are almost the same, except you'll be running the backend locally while using the database inside Docker.

1. **Clone the repository**  
   ```sh
   git clone -b dev git@github.com:4ikkamony/planetarium-api.git  
   ```
   ```sh
   cd planetarium-api  
   ```

2. **Configure virtual environment**
   ```sh
   python -m venv .venv
   ```
   **On Linux/MacOS(bash, zsh, etc)**
   ```sh
   source .venv/bin/activate 
   ```
   **On Windows(CMD)**
   ```sh
   .venv\Scripts\activate
   ```

3. **Install requirements**
   ```sh
   pip install -r requirements/dev.txt
   ```
   
5. **Set up environment variables**  
   ```sh
   mv docker/.env.sample docker/.env  
   ```
   - Fill in your [Stripe API Keys](https://support.stripe.com/questions/what-are-stripe-api-keys-and-how-to-find-them).  
   - Set **POSTGRES_HOST**=localhost to connect to the database container.  

6. **Start only the database container**  
   **On Linux**
   ```sh
   nohup docker compose -f docker/docker-compose-local.yaml up &
   ```
   **On Windows**
   ```sh
   start docker compose -f docker/docker-compose-local.yaml up
   ```

8. **Navigate to the source directory**  
   ```sh
   cd src  
   ```
   
9. **Apply migrations, load initial data, and run the server**  
   ```sh
   python manage.py migrate
   ```
   ```sh
   python manage.py loaddata data/planetarium_db_data.json
   ```
   ```sh
   python manage.py runserver  
   ```

11. **🧪 Run tests(when in src/)**   
   ```sh
   pytest
   ```  

[⬆️](#contents)

---

## 📖 After Installation  
Visit Swagger API Docs at http://127.0.0.1:8000/api/doc/swagger/ to see available endpoints and some example requests.

### Usage guide
#### Login
- If you have loaded the sample data, you can use these credentials:

  **Email**
  ```
  admin@example.com
  ```
  **Password**
  ```
  1qazcde3
  ```

- Built in Django Admin panel is available at http://127.0.0.1:8000/admin

- You can get JWT Token at http://127.0.0.1:8000/api/user/token/ endpoint.

    Although, most endpoints are available as readonly even for anonimous users.
    Except for http://127.0.0.1:8000/api/planetarium/bookings, where bookings of a currently logged in
    user are displayed.
  

🛠️ *Under construction...*

[⬆️](#contents)
