# Generated by Django 4.2.1 on 2023-05-20 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Оценка заказа'),
        ),
    ]
