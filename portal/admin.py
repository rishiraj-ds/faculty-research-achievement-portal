from django.contrib import admin
from .models import Profile, Record


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'designation')


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'record_type', 'year', 'status')
    list_filter = ('record_type', 'status', 'year')
    search_fields = ('title', 'faculty__username')
