# Generated by Django 5.2 on 2025-04-21 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_sessionverification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessionverification',
            options={'ordering': ['-created_at'], 'verbose_name': 'Session Verification', 'verbose_name_plural': 'Session Verifications'},
        ),
    ]
