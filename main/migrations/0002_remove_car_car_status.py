# Generated by Django 4.2.1 on 2023-05-22 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='car_status',
        ),
    ]
