# main/models.py
from django.db import models

class UserSubmission(models.Model):
    name           = models.CharField(max_length=100)
    unique_number  = models.CharField(max_length=20, blank=True)
    session_number = models.CharField(max_length=6,  blank=True)
    email          = models.EmailField(            blank=True)  # New field

    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} | {self.unique_number} | {self.session_number} | {self.email}"
