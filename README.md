Quick Start

Copy `.env.sample` to `.env` and fill the missing fields:
cp .env.sample .env

Build and run containers:
docker compose up --build

Create a superuser:
docker compose exec django-web python manage.py createsuperuser

Access API at http://localhost:8000/
Access Admin at http://localhost:8000/admin/

Run Tests:
docker compose exec django-web python manage.py test
