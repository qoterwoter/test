# Generated by Django 4.2.1 on 2023-05-21 18:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_order_price_driverresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='driverresponse',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
