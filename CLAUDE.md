# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server (--insecure serves static files without DEBUG=True issues)
python manage.py runserver --insecure

# Apply migrations (also seeds all sample data on first run)
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Run tests
python manage.py test

# Run tests for a single app
python manage.py test wardrobe
python manage.py test outfits
python manage.py test planner
python manage.py test core

# Lint and format with ruff
ruff check .
ruff format .
```

## Environment Setup

Copy `.env.example` to `.env` and fill in PostgreSQL credentials:

```
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=True
POSTGRES_DB=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

Generate a secret key: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

## Architecture

**4-app Django project** (`Wearly_Fashion_App/` is the Django project config dir):

- `core/` — Home page, shared mixins (`SetPaginateByMixin`), template tags, and `SeasonChoices`
- `wardrobe/` — `Brand` and `Garment` models with CRUD; `ImageSizeValidator` (max 5MB); slug auto-generated from `title + brand.name`
- `outfits/` — `Outfit` and `OutfitGarment` (M2M through model) linking garments to outfits
- `planner/` — `PlanEntry` model; one outfit per date (unique constraint); FK to `Outfit` with `PROTECT`

**Data relationships:**
- `Brand` → `Garment` (1:N, `on_delete=PROTECT`)
- `Garment` ↔ `Outfit` via `OutfitGarment` (M2M through table)
- `Outfit` → `PlanEntry` (1:N, `on_delete=PROTECT`)

**Deletion guards:** Both `GarmentDeleteView` and `BrandDeleteView` check for related objects and redirect with a `messages.error` instead of raising a DB error.

**URL routing:** All app URL configs are included at the root path `""` in `Wearly_Fashion_App/urls.py`; each app's `urls.py` uses its own `app_name` for namespacing.

**Views pattern:** List views inherit from both `SetPaginateByMixin`, `ListView`, and `FormView` to combine filtering forms with paginated querysets. Pagination-per-page is stored in session.

**Template tags** in `core/templatetags/`: `capitalize`, `cards`, `category_filter`, `collection_section`, `empty_collection`, `section_header` — used for reusable UI components across templates.

**Sample data:** `wardrobe/migrations/0007_seed_comprehensive_data.py` seeds brands, garments, outfits, and plan entries and copies images from `static/sample_images/` to `media/`. This runs automatically on `migrate`.

**Admin:** Uses `django-unfold` for an enhanced admin UI (configured before `django.contrib.admin` in `INSTALLED_APPS`).

**Static/Media:**
- Static files: `static/` (source) → `staticfiles/` (collected)
- Media uploads: `media/wardrobe/` and `media/outfits/`
- Sample images bundled in `static/sample_images/`