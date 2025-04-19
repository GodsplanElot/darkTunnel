from django.db import models

# Create your models here.

class Case(models.Model):
    case_id = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)