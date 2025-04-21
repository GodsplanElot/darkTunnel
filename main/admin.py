from django.contrib import admin
from .models import UserSubmission

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_number', 'session_number', 'created_at')
    search_fields = ('name', 'unique_number', 'session_number')
    list_filter = ('created_at',)