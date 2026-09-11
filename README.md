# Travel Discovery App

A small standalone Django app for capturing discovery responses from travel, tours and hospitality businesses. It uses a friendly multi-step public form and Django admin for reviewing submissions.

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

- Public form: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Supabase

Use the Supabase PostgreSQL connection string as `DATABASE_URL`.

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/postgres
```

No Supabase SDK is required. Django connects directly to PostgreSQL.

## Render

This project is configured for one Render web service only. There is no worker service.

Set these environment variables in Render:

```env
DJANGO_ENV=production
DATABASE_URL=your-supabase-database-url
ALLOWED_HOSTS=your-render-domain.onrender.com,your-custom-domain.com
CSRF_TRUSTED_ORIGINS=https://your-render-domain.onrender.com,https://your-custom-domain.com
```

Render generates `SECRET_KEY` from `render.yaml`.

## Checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py collectstatic --noinput
```
