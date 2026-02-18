<div align="center">

# 👗 Wearly Fashion App

**Your Personal Digital Wardrobe & Outfit Planner**

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
</div>

---

## 📋 Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Setup Instructions for Lecturers](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#-project-structure)
- [Database Schema](#database-schema)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#contact)

---

## About

**Wearly** is a full-featured Django web application designed to help users organize their wardrobe, create stylish outfits, and plan their weekly looks. Built as a course project for SoftUni's Django Basics course, it demonstrates comprehensive Django development including multi-app architecture, reusable templates, custom template tags/filters, form validation, class-based views, and modern UI design with glass-morphism aesthetics.

### Why Wearly?

- **Organize** your clothing items by brand, category, season, and more
- **Build** complete outfits by combining garments
- **Plan** your weekly wardrobe with the outfit planner
- **Search & Filter** through your collection effortlessly
- **Responsive Design** that works on all devices
- **Modern UI** with glass-morphism aesthetic

---

## Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **Wardrobe Management** | Full CRUD for brands and garments with categories, seasons, pricing, and images |
| **Outfit Builder** | Create and manage outfits by combining multiple garments with many-to-many relationships |
| **Weekly Planner** | Schedule outfits for specific dates with personal notes and planning insights |
| **Smart Search & Filter** | Advanced filtering by brand, category, season with multi-sort options |
| **Brand Management** | Track clothing brands with statistics and related garments |

### Technical Highlights

- ✅ Multi-app Django architecture (4 apps: core, wardrobe, outfits, planner)
- ✅ PostgreSQL database with optimized relationships
- ✅ Class-based views (CBV)
- ✅ Custom template tags and filters for dynamic content
- ✅ Reusable template partials and inheritance (DRY principles)
- ✅ Form validation with custom validators and user-friendly error messages
- ✅ Image upload with size validation (max 5MB) using Pillow
- ✅ Responsive glass-morphism UI design using CSS3
- ✅ Data migrations for automatic sample data seeding with pre-uploaded images
- ✅ Custom 404 error page with navigation
- ✅ Complete CRUD functionality for multiple models
- ✅ OOP principles and clean code architecture

---

## Tech Stack

| Category | Technologies |
|----------|--------------|
| **Backend** | Python 3.13, Django 6.0 |
| **Database** | PostgreSQL 16 |
| **Frontend** | HTML5, CSS3 (Glass-morphism design) |
| **Image Processing** | Pillow 12.1.0 |
| **Environment** | python-dotenv 1.2.1 |
| **Server** | Gunicorn-ready (ASGI/WSGI) |

---

## Installation

### Prerequisites

- Python 3.13+
- PostgreSQL 16+
- Git
- Virtual Environment (recommended)

### Quick Setup (For Lecturers)

**The simplest way to get started:**

```bash
# 1. Clone the repository
git clone https://github.com/ivxn1/Wearly_Fashion_App.git
cd wearly-fashion-app

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Configure database (copy and edit environment file)
cp .env.example .env

# 5. Edit .env file with your PostgreSQL credentials:
# POSTGRES_DB=wearly_db
# POSTGRES_USER=your_username
# POSTGRES_PASSWORD=your_password
# POSTGRES_HOST=localhost
# POSTGRES_PORT=5432

# 6. Apply migrations (this automatically seeds all sample data and copies images)
python manage.py migrate

# 7. Run the development server
python manage.py runserver

# 8. Open in browser
# Navigate to: http://127.0.0.1:8000/
```

**That's it!** The application is ready with sample data and all images pre-loaded.

---

## Setup Instructions

### What Happens During Setup

When you run `python manage.py migrate`, the following occurs automatically:

1. ✅ Database tables are created for all models
2. ✅ Sample data is inserted into the database:
   - 10 fashion brands (Nike, Adidas, Zara, H&M, Levi's, etc.)
   - 35+ garments across all categories with complete properties
   - 8 complete outfits for various occasions
   - 14+ planned outfit entries for the week
3. ✅ All images are copied from `static/sample_images/` to `media/` directories
4. ✅ Images are automatically converted/copied to ensure compatibility

### Database Location & Image Handling

- **Generated Media**: `/media/wardrobe/` and `/media/outfits/` directories
- **Pre-uploaded Sample Images**: `/static/sample_images/`
  - `/static/sample_images/clothes/` - Organized by garment category
  - `/static/sample_images/outfits/` - Outfit photos

The migration uses the pre-downloaded fashion images included in the project, **no internet connection required**.

### Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=True

# PostgreSQL Database Configuration
POSTGRES_DB=wearly_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

> 💡 **Generate a secret key:**
> ```bash
> python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
> ```

---

## Usage

### Main Pages & URLs

| Page | URL | Description |
|------|-----|-------------|
| **Home** | `/` | Dashboard with featured items and statistics |
| **Garments List** | `/garments/` | Browse all garments with advanced search & filtering |
| **Garment Details** | `/garments/<slug>/` | View detailed garment information |
| **Add Garment** | `/garments/add/` | Create a new garment (CRUD Create) |
| **Edit Garment** | `/garments/<slug>/edit/` | Modify garment details (CRUD Update) |
| **Delete Garment** | `/garments/<slug>/delete/` | Remove garment with confirmation (CRUD Delete) |
| **Outfits List** | `/outfits/` | View all outfit combinations |
| **Outfit Details** | `/outfits/<slug>/` | See outfit composition and garments |
| **Add Outfit** | `/outfits/add/` | Create new outfit with multiple garments |
| **Edit Outfit** | `/outfits/<slug>/edit/` | Modify outfit details |
| **Delete Outfit** | `/outfits/<slug>/delete/` | Remove outfit with confirmation |
| **Weekly Planner** | `/planner/` | View planned outfits for the week |
| **Add Plan Entry** | `/planner/add/` | Schedule an outfit for a specific date |
| **Edit Plan Entry** | `/planner/<id>/edit/` | Update planned outfit |
| **Delete Plan Entry** | `/planner/<id>/delete/` | Remove scheduled outfit |
| **Brands List** | `/brands/` | View all brands with statistics |
| **Brand Details** | `/brands/<slug>/` | See brand details and related garments |
| **Add Brand** | `/brands/add/` | Create new brand |
| **Edit Brand** | `/brands/<slug>/edit/` | Modify brand information |
| **Delete Brand** | `/brands/<slug>/delete/` | Remove brand (only if no garments assigned) |
| **Custom 404** | Any invalid URL | User-friendly error page with navigation |

---

## 📁 Project Structure

```
wearly-fashion-app/
│
├── 📂 core/                        # Core application (home, base templates)
│   ├── templatetags/               # Custom template tags & filters
│   │   ├── capitalize.py           # Capitalize text filter
│   │   ├── cards.py                # Reusable card components
│   │   ├── category_filter.py      # Category display helpers
│   │   ├── collection_section.py   # Collection layout tags
│   │   ├── empty_collection.py     # Empty state templates
│   │   └── section_header.py       # Section header component
│   ├── views.py                    # Home page and core views
│   ├── admin.py                    # Django admin configuration
│   ├── models.py                   # Shared models (Season choices)
│   ├── choices.py                  # Global choice definitions
│   └── urls.py                     # Core URL routing
│
├── 📂 wardrobe/                    # Wardrobe management app
│   ├── migrations/                 # Database migration files
│   │   └── 0007_seed_comprehensive_data.py  # Data seeding migration
│   ├── models.py                   # Brand & Garment models
│   ├── forms.py                    # Brand/Garment forms & validators
│   ├── views.py                    # Class-based CRUD views
│   ├── validators.py               # Custom field validators (ImageSizeValidator)
│   ├── choices.py                  # Garment category choices
│   └── urls.py                     # Wardrobe URL routing
│
├── 📂 outfits/                     # Outfit builder app
│   ├── migrations/                 # Database migration files
│   ├── models.py                   # Outfit & OutfitGarment models
│   ├── forms.py                    # Outfit creation/edit forms
│   ├── views.py                    # Outfit CRUD views
│   └── urls.py                     # Outfit URL routing
│
├── 📂 planner/                     # Weekly planner app
│   ├── migrations/                 # Database migration files
│   ├── models.py                   # PlanEntry model
│   ├── forms.py                    # Plan entry forms
│   ├── views.py                    # Planner views
│   └── urls.py                     # Planner URL routing
│
├── 📂 templates/                   # HTML templates (Django Template Engine)
│   ├── base.html                   # Base template with navigation & footer
│   ├── 404.html                    # Custom 404 error page
│   ├── core/
│   │   ├── home.html               # Home page dashboard
│   │   └── partials/               # Reusable template components
│   │       ├── hero.html           # Hero section partial
│   │       ├── footer.html         # Footer partial
│   │       ├── navbar.html         # Navigation bar
│   │       └── ...
│   ├── wardrobe/                   # Brand & Garment templates
│   │   ├── garment_list.html       # Garment list with search
│   │   ├── garment_details.html    # Garment detail view
│   │   ├── garment_form.html       # Garment create/edit form
│   │   ├── garment_confirm_delete.html
│   │   ├── brand_list.html
│   │   ├── brand_details.html
│   │   ├── brand_form.html
│   │   └── brand_confirm_delete.html
│   ├── outfits/                    # Outfit templates
│   │   ├── outfit_list.html
│   │   ├── outfit_details.html
│   │   ├── outfit_form.html
│   │   └── outfit_confirm_delete.html
│   └── planner/                    # Planner templates
│       ├── planner.html
│       ├── plan_entry_form.html
│       └── plan_confirm_delete.html
│
├── 📂 static/                      # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── base.css                # Base styling & glass-morphism
│   │   ├── home.css                # Home page styles
│   │   ├── form-page.css           # Form styling (general)
│   │   ├── outfit-form.css         # Outfit form specific styles
│   │   ├── planner.css             # Planner-specific styles
│   │   └── 404.css                 # Error page styles
│   ├── scripts/
│   │   └── form-handler.js         # Form interactions and validations
│   ├── sample_images/              # Pre-downloaded sample images (NO internet needed)
│   │   ├── clothes/                # Garment images by category
│   │   │   ├── tshirts/
│   │   │   ├── shirts/
│   │   │   ├── jeans/
│   │   │   ├── shorts/
│   │   │   ├── sweaters/
│   │   │   ├── jackets/
│   │   │   ├── coats/
│   │   │   ├── shoes/
│   │   │   ├── accessories/
│   │   │   └── hats/
│   │   └── outfits/                # Outfit category images
│   └── images/                     # Brand logos & UI images
│
├── 📂 media/                       # User-uploaded media (generated at runtime)
│   ├── wardrobe/                   # Garment images (created during migration)
│   └── outfits/                    # Outfit images (created during migration)
│
├── 📂 Wearly_Fashion_App/          # Django project settings
│   ├── settings.py                 # Project configuration
│   ├── urls.py                     # Main URL router
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application
│
├── manage.py                       # Django management script
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
└── README.md                       # This file
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐          ┌──────────────────┐          ┌─────────────┐
│     Brand       │◄─────────│     Garment      │◄────┬────│    Outfit   │
├─────────────────┤   1:N    ├──────────────────┤     │    ├─────────────┤
│ id (PK)         │          │ id (PK)          │     │    │ id (PK)     │
│ name (UNIQUE)   │  PROTECT │ title            │     │    │ title       │
│ website (URL)   │          │ category         │     M:M  │ occasion    │
│ country         │          │ color            │     │    │ season      │
└─────────────────┘          │ size             │     │    │ notes       │
                             │ material         │     │    │ image       │
                             │ season           │     │    │ created_at  │
                             │ price            │     │    └──────┬──────┘
                             │ image            │     │           │
                             │ brand_id (FK)    │     │           │1:N PROTECT
                             │ slug             │     │           │
                             │ created_at       │     │           │
                             └────────┬─────────┘     │    ┌──────▼────────┐
                                      │               │    │  PlanEntry    │
                                      └────────┬──────┘    ├───────────────┤
                                             M:M           │ id (PK)       │
                                    OutfitGarment table    │ date (UNIQUE) │
                                      ┌──────────────┐     │ outfit_id(FK) │
                                      │ id (PK)      │     │ note          │
                                      │ outfit_id(FK)│     │ created_at    │
                                      │ garment_id(FK)     └───────────────┘
                                      └──────────────┘
```

### Models & Relationships

**1. Brand**
- One-to-Many with Garment (one brand can have many garments)
- Protected deletion (cannot delete brand if garments exist)
- Fields: name, website, country

**2. Garment**
- Foreign Key to Brand
- Many-to-Many with Outfit (through OutfitGarment)
- Categories: T-shirts, Shirts, Jeans, Shorts, Sweaters, Jackets, Coats, Shoes, Accessories, Hats
- Fields: title, category, color, size, material, season, price, image, slug, created_at

**3. Outfit**
- Many-to-Many with Garment (through OutfitGarment)
- One-to-Many with PlanEntry
- Protected deletion from PlanEntry
- Fields: title, occasion, season, notes, image, created_at

**4. OutfitGarment** (Through Model)
- Links Outfit and Garment with many-to-many relationship

**5. PlanEntry**
- Foreign Key to Outfit
- One entry per date (unique constraint)
- Protected deletion
- Fields: date, outfit, note, created_at

---

## Key Features in Detail

### Sample Data Included

The application comes pre-populated with realistic sample data:

| Resource | Count | Notes |
|----------|-------|-------|
| Brands | 10 | Nike, Adidas, Zara, H&M, Levi's, Uniqlo, The North Face, Ralph Lauren, Tommy Hilfiger, Calvin Klein |
| Garments | 35+ | All categories, colors, sizes, seasons, and price ranges |
| Outfits | 8 | Business, casual, gym, beach, date night, weekend, formal, and weekend brunch |
| Outfit-Garment Links | 33+ | Complete outfit compositions |
| Plan Entries | 14+ | Next two weeks of planned outfits with notes |

**All images are pre-downloaded and included in the project** - no internet required for setup!

### Search & Filter System

- **Advanced Search**: Filter by brand, category, season
- **Multi-sort Options**: Price (low-high, high-low), newest, alphabetical
- **Category Headers**: Visual separation by garment type
- **Dynamic Filtering**: Real-time results as you adjust filters
- **Responsive Layout**: Works on mobile, tablet, and desktop

### Garment Management

- Create garments with image upload (max 5MB)
- Categorize by type, color, material, season
- Track price and brand association
- Edit and delete with confirmation
- View garment details and usage in outfits
- Slug-based URLs for clean routing

### Outfit Builder

- Combine multiple garments into outfits
- Select garments via interactive cards
- Add occasion and season information
- Include notes and styling tips
- View complete outfit compositions
- Delete with confirmation

### Weekly Planner

- Schedule outfits for specific dates
- Add personal notes for each day
- View full week at a glance
- One outfit per day (unique date constraint)
- Delete with visual date preview
- Organized by date

### Brand Management

- Create new brands with website and country info
- View brand details and statistics
- See all garments associated with a brand
- Cannot delete brands with assigned garments
- Delete with confirmation
- Track brand popularity

---

## Development

### Custom Validators

All custom validators are in `wardrobe/validators.py`:
- **ImageSizeValidator**: Ensures images don't exceed 5MB

### Template Tags

Located in `core/templatetags/`:
- `capitalize`: Text filter for capitalization
- `cards`: Reusable card components
- `category_filter`: Display category names
- `collection_section`: Layout for collections
- `empty_collection`: Empty state messaging
- `section_header`: Consistent section headers

### Forms & Validation

- Custom form fields with enhanced validation
- User-friendly error messages
- Read-only fields where appropriate
- Form-based field exclusion for create vs. edit forms
- Pre-population of related choices

---

## Contributing

This is a course project, but here's the development workflow:

```bash
# Create a feature branch
git checkout -b feature/your-feature

# Make your changes and commit
git add .
git commit -m 'Add: description of feature'

# Push to repository
git push origin feature/your-feature
```

### Code Standards
- Follow PEP 8 style guidelines
- Write meaningful commit messages
- Add docstrings to models and views
- Test changes before committing
- Maintain DRY (Don't Repeat Yourself) principles
- Use class-based views where appropriate

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for full details.

MIT License permits:
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use

**Conditions:**
- Include license and copyright notice in distributions

---

## Contact

**Ivan Zhelev**

- 📧 Email: [ivxn.zhelev@gmail.com](mailto:ivxn.zhelev@gmail.com)
- 💼 GitHub: [@ivanzhelev](https://github.com/ivanzhelev)
- 🎓 SoftUni: Django Basics Course

---

<div align="center">

### ⭐ Star this repo if you found it helpful!

</div>

