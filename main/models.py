from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class CarDocument(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=('дата создания'))
    driver_license = models.CharField(max_length=50, verbose_name=('водительские права'))
    world_license = models.CharField(max_length=50, verbose_name=('международные права'))
    registration = models.CharField(max_length=50, verbose_name=('регистрация'))
    car_status = models.CharField(max_length=50, verbose_name=('статус автомобиля'))

    def __str_(self):
        return ""

    class Meta:
        verbose_name = ('Документы на машину')
        verbose_name_plural = ('Документы на машины')


class Car(models.Model):
    name = models.CharField(max_length=50, verbose_name=('название'))
    car_photo_path = models.CharField(max_length=100, verbose_name=('Фото автомобиля'))
    car_document_id = models.ForeignKey(CarDocument, on_delete=models.CASCADE, verbose_name=('документы автомобиля'))

    def __str_(self):
        return self.name

    class Meta:
        verbose_name = ('Машина')
        verbose_name_plural = ('Машины')


class Driver(models.Model):
    name = models.CharField(max_length=50, verbose_name=('имя'))
    rating = models.IntegerField(verbose_name=('рейтинг'))
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name=('автомобиль'), null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('пользователь'), blank=True, limit_choices_to={'is_staff': True})

    def __str_(self):
        return self.name

    class Meta:
        verbose_name = ('Водитель')
        verbose_name_plural = ('Водители')


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('P', ('Ожидание')),
        ('A', ('Принят')),
        ('C', ('Отменен')),
        ('F', ('Завершен')),
    ]
    from_location = models.CharField(max_length=100, verbose_name=('откуда'))
    to_location = models.CharField(max_length=100, verbose_name=('куда'))
    arrive_time = models.DateTimeField(verbose_name=('время прибытия'))
    departure_time = models.DateTimeField(verbose_name=('время отправления'))
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('клиент'))
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, verbose_name=('водитель'), null=True, blank=True)
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default='P',
                                    verbose_name=('статус заказа'), null=True, blank=True)
    men_amount = models.IntegerField(verbose_name=('количество взрослых'))
    children_amount = models.IntegerField(verbose_name=('количество детей'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=('дата создания'))
    comment = models.TextField(verbose_name=('комментарий'))

    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')

    def __str_(self):
        return f"{self.from_location} - {self.to_location} ({self.departure_time})"


class Feedback(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('клиент'))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=('заказ'))
    rating = models.IntegerField(verbose_name=('оценка'))
    comment = models.TextField(verbose_name=('комментарий'))

    def __str_(self):
        return f"{self.client.username} - {self.order}"

    class Meta:
        verbose_name = ('Отзыв')
        verbose_name_plural = ('Отзывы')


@receiver(post_save, sender=User)
def create_driver(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Driver.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
