# Generated by Django 4.2.1 on 2023-06-20 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_driver_car_alter_driver_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='notifications',
            field=models.BooleanField(default=True, verbose_name='Уведомления'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='rating',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='рейтинг'),
        ),
        migrations.AlterField(
            model_name='driverresponse',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Выбран пользователем'), ('n', '')], default='n', max_length=1, null=True, verbose_name='Статус'),
        ),
    ]
