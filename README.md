# Django Catalog App

Personal Django learning project following the MDN tutorial (locallibrary app, static files, deployment-ready).

## Features
- Book catalog app (`catalog`)
- Static files handled with **Whitenoise**
- Custom management command for seeding database data
- Deployment-ready configuration

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/adupoku71/locallibrary-django.git
   cd locallibrary-django
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
3. Run migrations:
   ```bash
   python manage.py migrate

4. Seed the database with sample data:
   ```bash
    python manage.py seed_data

5. Run the development server:
    ```bash
    python manage.py runserver

## Deployment
- Configured with Whitenoise for static file serving.
- Run python manage.py collectstatic before deploying.
