from django.contrib import admin
from .models import UserSubmission
# Register your models here.
# main/admin.py


@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'unique_number', 'created_at')
    search_fields = ('name', 'unique_number')
    list_filter = ('created_at',)