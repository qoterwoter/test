from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
import datetime


class CarDocument(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=('дата создания'))
    driver_license = models.CharField(max_length=50, verbose_name=('водительские права'))
    world_license = models.CharField(max_length=50, verbose_name=('международные права'))
    registration = models.CharField(max_length=50, verbose_name=('регистрация'))
    car_status = models.CharField(max_length=50, verbose_name=('статус автомобиля'))

    def __str__(self):
        return f"{self.pk} Document"

    class Meta:
        verbose_name = ('Документы на машину')
        verbose_name_plural = ('Документы на машины')


class Car(models.Model):
    name = models.CharField(max_length=50, verbose_name=('название'))
    car_photo_path = models.CharField(max_length=100, verbose_name=('Фото автомобиля'))
    car_document_id = models.ForeignKey(CarDocument, on_delete=models.CASCADE, verbose_name=('документы автомобиля'))

    def __str__(self):
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
    from_location = models.CharField(max_length=100, verbose_name=('откуда'))
    to_location = models.CharField(max_length=100, verbose_name=('куда'))
    departure_time = models.DateTimeField(verbose_name=('время отправления'))
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('клиент'))
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, verbose_name=('водитель'), null=True, blank=True)
    men_amount = models.IntegerField(verbose_name=('количество взрослых'))
    children_amount = models.IntegerField(verbose_name=('количество детей'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=('дата создания'))
    comment = models.TextField(verbose_name=('комментарий'))
    price = models.IntegerField(verbose_name='Стоимость', null=True, blank=True)

    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')

    def __str_(self):
        return f"{self.from_location} - {self.to_location} ({self.departure_time})"


class DriverResponse(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    price = models.IntegerField(verbose_name='Стоимость', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(default=datetime.timedelta(hours=0))

    class Meta:
        verbose_name = ('Отклик на заказ')
        verbose_name_plural = ('Отклики на заказы')


class OrderRating(models.Model):
    communication_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Коммуникация')
    driver_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Водитель')
    transport_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],verbose_name='Транспорт')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ')

    class Meta:
        verbose_name = ('Оценка заказа')
        verbose_name_plural = ('Оценки заказов')
        unique_together = ('order',)  # make order field unique


class Feedback(models.Model):
    STATUS_CHOICE = (
        ('publish', 'Опубликован'),
        ('on_moder', 'На обработке'),
        ('hiden', 'Скрыт')
    )
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('клиент'))
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],verbose_name='Оценка')
    comment = models.TextField(verbose_name=('комментарий'))
    status = models.CharField(choices=STATUS_CHOICE, verbose_name='Статус отзыва', max_length=8, default='on_moder')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')

    def __str_(self):
        return f"{self.client.username} - {self.rating}"

    class Meta:
        verbose_name = ('Отзыв')
        verbose_name_plural = ('Отзывы')


class SupportRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('ongoing', 'В работе'),
        ('resolved', 'Решен'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = ('Запрос в техподдержку')
        verbose_name_plural = ('Запросы в техподдержку')


@receiver(post_save, sender=User)
def create_driver(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Driver.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
