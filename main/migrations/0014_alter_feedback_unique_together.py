# Generated by Django 4.2.1 on 2023-05-21 11:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_alter_feedback_rating_alter_feedback_status'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together={('client',)},
        ),
    ]
