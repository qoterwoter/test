# Generated by Django 4.2.1 on 2023-05-21 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_remove_order_arrive_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Стоимость'),
        ),
        migrations.CreateModel(
            name='DriverResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Стоимость')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.driver')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.order')),
            ],
            options={
                'verbose_name': 'Отклик на заказ',
                'verbose_name_plural': 'Отклики на заказы',
            },
        ),
    ]
