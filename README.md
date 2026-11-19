# Faculty Research and Achievement Management Portal (Django)

## Setup (run in an empty folder)
    python -m venv venv
    venv\Scripts\activate            (Mac/Linux: source venv/bin/activate)
    pip install django
    django-admin startproject config .
    -> now extract faculty_portal.zip INTO this same folder and choose "overwrite"
       (it replaces config/settings.py and config/urls.py and adds portal/ and templates/)
    python manage.py makemigrations portal
    python manage.py migrate
    python manage.py seed             (demo users + records)
    python manage.py runserver

Open http://127.0.0.1:8000

## Logins created by `seed`
- HOD / Admin: hod / hod12345   (can review, see reports, export CSV, open /admin)
- Faculty: anil, sita, ravi / faculty123
