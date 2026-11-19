from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.department})"


class Record(models.Model):
    TYPES = [
        ('publication', 'Publication'),
        ('project', 'Research Project / Grant'),
        ('patent', 'Patent'),
        ('award', 'Award'),
        ('event', 'FDP / Workshop / Talk'),
    ]
    STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    record_type = models.CharField('Type', max_length=20, choices=TYPES)
    title = models.CharField(max_length=300)
    details = models.TextField(blank=True, help_text='Journal / agency / venue, DOI, amount, etc.')
    year = models.PositiveIntegerField()
    proof = models.FileField('Proof (PDF / image)', upload_to='proofs/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
