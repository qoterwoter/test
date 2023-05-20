# Generated by Django 4.2.1 on 2023-05-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_supportrequest_request_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportrequest',
            name='request_status',
        ),
        migrations.AddField(
            model_name='supportrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'В ожидании'), ('ongoing', 'В работе'), ('resolved', 'Решен')], default='pending', max_length=20),
        ),
    ]