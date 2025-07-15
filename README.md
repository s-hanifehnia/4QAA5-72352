Quick Start

Copy `.env.sample` to `.env` and fill the missing fields:
```bash
cp .env.sample .env
```

Build and run containers:
```bash
docker compose up --build
```

Create a superuser:
```bash
docker compose exec django-web python manage.py createsuperuser
```

Access API at http://localhost:8000/

Access Swagger at http://localhost:8000/swagger/

Access Admin at http://localhost:8000/admin/

Run Tests:
```bash
docker compose exec django-web python manage.py test
```
