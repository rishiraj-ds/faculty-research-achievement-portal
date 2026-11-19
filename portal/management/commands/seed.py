from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from portal.models import Profile, Record


class Command(BaseCommand):
    help = 'Create demo users and records for the project demo'

    def handle(self, *args, **options):
        hod, _ = User.objects.get_or_create(username='hod', defaults={
            'first_name': 'Hema', 'last_name': 'Rao', 'is_staff': True, 'is_superuser': True})
        hod.set_password('hod12345')
        hod.save()
        Profile.objects.get_or_create(user=hod, defaults={'department': 'Computer Science', 'designation': 'HOD'})

        faculty = [
            ('anil', 'Anil', 'Kumar', 'Computer Science', 'Associate Professor'),
            ('sita', 'Sita', 'Devi', 'Computer Science', 'Assistant Professor'),
            ('ravi', 'Ravi', 'Teja', 'Electronics', 'Professor'),
        ]
        users = []
        for username, first, last, dept, desig in faculty:
            u, _ = User.objects.get_or_create(username=username, defaults={'first_name': first, 'last_name': last})
            u.set_password('faculty123')
            u.save()
            Profile.objects.get_or_create(user=u, defaults={'department': dept, 'designation': desig})
            users.append(u)

        data = [
            (0, 'publication', 'Deep Learning for Crop Disease Detection', 2024, 'IEEE Access, Scopus indexed, DOI 10.1109/demo.1', 'approved'),
            (0, 'publication', 'Federated Learning in Healthcare', 2025, 'Springer LNCS, Scopus indexed', 'approved'),
            (0, 'project', 'Smart Campus IoT Platform', 2023, 'DST, Rs. 8,50,000, 2 years', 'approved'),
            (0, 'award', 'Best Paper Award', 2025, 'ICCCNT 2025', 'pending'),
            (1, 'publication', 'Sentiment Analysis of Regional Languages', 2024, 'Elsevier, SCI indexed', 'approved'),
            (1, 'event', 'FDP on Cloud Computing', 2025, 'Attended, 5 days, JNTU Hyderabad', 'pending'),
            (1, 'patent', 'Low-cost Attendance Monitoring Device', 2024, 'Filed, Indian Patent Office', 'rejected'),
            (2, 'publication', 'Low Power VLSI Design Techniques', 2023, 'IJERT', 'approved'),
            (2, 'project', 'Embedded Systems for Agriculture', 2024, 'AICTE, Rs. 5,00,000', 'approved'),
            (2, 'event', 'Guest Lecture on 5G Networks', 2025, 'Delivered at NIT Warangal', 'pending'),
        ]
        for idx, rtype, title, year, details, status in data:
            Record.objects.get_or_create(faculty=users[idx], title=title, defaults={
                'record_type': rtype, 'year': year, 'details': details, 'status': status})

        self.stdout.write(self.style.SUCCESS(
            'Demo data ready. HOD login: hod / hod12345. Faculty logins: anil, sita, ravi / faculty123'))
