# Wearly Fashion App

A Django web application for managing a personal wardrobe, building outfits, and planning weekly looks. Built as a final project for SoftUni's Django Advanced course.

**Live demo:** [https://wearly-app.com](https://wearly-app.com)

## Tech Stack

- Python 3.13, Django 6.0
- PostgreSQL
- Celery + Redis (async tasks, scheduled jobs)
- Django REST Framework (API endpoints)
- Cloudinary (media storage in production)
- WhiteNoise (static files)
- Resend (transactional email in production)
- Deployed on Railway

## Prerequisites

- Python 3.13+
- Docker Desktop (for PostgreSQL and Redis)
- Git

## Setup

```bash
git clone https://github.com/ivxn1/Wearly_Fashion_App.git
cd Wearly_Fashion_App

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env

docker compose up -d

python manage.py migrate

python manage.py runserver --insecure
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### Demo User

A demo user is seeded automatically on first migration:

| Field    | Value          |
|----------|----------------|
| Email    | seed@wearly.app |
| Password | demo123        |

### Celery Workers (optional)

Async features (premium activation emails, weekly digest) require Celery workers. The docker-compose file starts them automatically alongside Redis.

To skip Celery entirely, add `CELERY_TASK_ALWAYS_EAGER=True` to your `.env` file. Tasks will run synchronously.

### Email

In production, transactional email is delivered via the Resend HTTP API (Railway blocks outbound SMTP). The custom backend at `core.email_backend.ResendEmailBackend` is enabled by setting `EMAIL_BACKEND=core.email_backend.ResendEmailBackend` and `RESEND_API_KEY` in the environment.

In local/demo mode the default `EMAIL_BACKEND` is `django.core.mail.backends.console.EmailBackend`. When a Celery task attempts to send an email (premium activation, password reset, weekly digest), the rendered HTML template and its context data are printed to the **Celery worker logs** instead of being delivered. This makes it easy to inspect the full message body without configuring a real email provider.

### Environment Variables

The `.env.example` file contains all required variables with working defaults for local development. Key settings:

| Variable | Purpose | Default |
|----------|---------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Dev key provided |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `POSTGRES_*` | Database connection | Matches docker-compose |
| `REDIS_URL` | Celery broker | `redis://localhost:6379/0` |
| `EMAIL_BACKEND` | Email backend | Console (prints to terminal) |
| `CLOUDINARY_*` | Media storage | Empty (uses local filesystem) |
| `RESEND_API_KEY` | Transactional email API | Empty (not needed locally) |

## Architecture

Five Django apps with clearly defined responsibilities:

| App | Purpose |
|-----|---------|
| `accounts` | Custom user model (AbstractBaseUser), profile, authentication, premium membership |
| `wardrobe` | Brand and Garment models with CRUD, image upload, search/filter |
| `outfits` | Outfit builder with M2M garment relationships, Style Boards |
| `planner` | Daily outfit scheduling with unique date constraints |
| `core` | Home page, shared mixins, custom template tags, error pages |

### Models and Relationships

- **Brand** -> Garment (1:N, PROTECT)
- **Garment** <-> Outfit via OutfitGarment (M2M through table)
- **Outfit** -> PlanEntry (1:N, PROTECT)
- **Outfit** <-> StyleBoard (M2M)
- **Wishlist** <-> Garment (M2M)
- **FavouriteOutfits** <-> Outfit (M2M)
- **CustomerUser** <-> CustomerProfileModel (1:1, signal-created)

### User Groups and Permissions

Two groups with distinct permissions enforced via `PermissionRequiredMixin`:

- **Member** -- standard CRUD on wardrobe, outfits, planner
- **Premium Member** -- everything above plus `can_trigger_digest` and `can_create_styleboard`

Users are auto-assigned to Member on registration. Premium activation adds the Premium Member group.

### Async Processing

Celery tasks with Redis broker:

- `send_premium_registration_email` -- async email with signed activation token
- `send_password_reset_email` -- async password reset dispatch
- `send_weekly_digest` -- HTML email with upcoming week's planned outfits
- `send_weekly_digest_to_all_premiums` -- fan-out task, scheduled via Celery Beat (Mondays 10 AM)

### REST API

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/wardrobe/` | GET | Required | List garments |
| `/api/outfits/` | GET | Required | List outfits |

### Sample Data

Running `migrate` automatically seeds:

- 10 brands, 35 garments, 8 outfits with garment compositions
- Demo user with profile
- Member and Premium Member groups with permissions
- All sample images copied to media storage

## Running Tests

```bash
python manage.py test
```

42 tests covering models, views, forms, signals, and permissions across all apps.

## Deployment

Deployed on Railway with five services:

- **Web** -- Gunicorn serving the Django app
- **Celery Worker** -- processes async tasks
- **Celery Beat** -- scheduled task dispatcher
- **PostgreSQL** -- managed database
- **Redis** -- Celery message broker

Static files served via WhiteNoise. Media files stored on Cloudinary. Transactional email via Resend HTTP API (Railway blocks outbound SMTP).

## Commands Reference

```bash
python manage.py runserver --insecure   # Dev server with static files
python manage.py test                   # Run test suite
python manage.py migrate                # Apply migrations + seed data
python manage.py makemigrations         # Generate new migrations
python manage.py reseed_images          # Re-upload seed images to storage backend
ruff check .                            # Lint
ruff format .                           # Format
```
