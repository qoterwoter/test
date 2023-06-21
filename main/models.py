from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db.models import Avg
from .utils import send_notification_email, send_driver_notifications


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, phoneNumber, is_staff, **extra_fields):
        email = self.normalize_email(email)
        first_name = extra_fields.pop('first_name', '')
        last_name = extra_fields.pop('last_name', '')
        user = self.model(
            username=username,
            email=email,
            phoneNumber=phoneNumber,
            is_staff=is_staff,
            **extra_fields)
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    phoneNumberRegex = RegexValidator(regex=r'^\+{1}[7]{1}\s{1}\(\d{3}\)\s{1}\d{3}\s{1}\d{2}\s{1}\d{2}$', message="Phone number must be in the format +7 (XXX) XXX XX XX")
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 18, verbose_name='Номер телефона')
    groups = models.ManyToManyField(Group, blank=True, related_name='users_in_group')

    objects = UserManager()

    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='users_with_permission',
        verbose_name=('user permissions'),
        help_text=(
            'Specific permissions for this user.'),
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Car(models.Model):
    CAR_STATUS_CHOICES = [
        ('on_moderate', 'Ждет обработки'),
        ('moderating', 'В обработке'),
        ('approved', 'Одобрено')
    ]
    name = models.CharField(max_length=50, verbose_name=('название'))
    car_photo_path = models.ImageField(upload_to='car_photos', verbose_name=('Фото автомобиля'))
    car_pass = models.ImageField(upload_to='car_pass', verbose_name='Регистрация ТС')
    photo_with_car_pass = models.ImageField(upload_to='photo_with_car_pass', verbose_name=('Фото с правами'))
    taxi_license = models.ImageField(upload_to='taxi_licesnse', verbose_name='Лицензия на перевозку')
    car_status = models.CharField(max_length=50, verbose_name=('статус автомобиля'), choices=CAR_STATUS_CHOICES, default='on_moderate')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('Машина')
        verbose_name_plural = ('Машины')


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.IntegerField(verbose_name=('рейтинг'), default=0, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name=('автомобиль'), null=True, blank=True, limit_choices_to={'car_status': 'approved'})
    notifications = models.BooleanField(default=False, verbose_name='Уведомления')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}, {self.rating} ★"

    class Meta:
        verbose_name = ('Водитель')
        verbose_name_plural = ('Водители')

    def update_rating(self):
        avg_rating = self.ratings.filter(driver_rating__isnull=False).aggregate(Avg('driver_rating'))['driver_rating__avg']
        self.rating = avg_rating if avg_rating else 0
        self.save()


class Order(models.Model):
    from_location = models.CharField(max_length=100, verbose_name=('откуда'))
    to_location = models.CharField(max_length=100, verbose_name=('куда'))
    departure_time = models.DateTimeField(verbose_name=('время отправления'))
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('клиент'), null=True, blank=True)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, verbose_name=('водитель'), null=True, blank=True)
    men_amount = models.IntegerField(verbose_name=('количество взрослых'))
    children_amount = models.IntegerField(verbose_name=('количество детей'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=('дата создания'))
    comment = models.TextField(verbose_name=('комментарий'), null=True, blank=True)
    price = models.IntegerField(verbose_name='Стоимость', null=True, blank=True)

    class Meta:
        verbose_name = ('Заказ')
        verbose_name_plural = ('Заказы')

    def __str__(self):
        return f"Заказ №{self.id}. {self.from_location} - {self.to_location} ({self.departure_time.strftime('%Y %m %d в %H:%M')})"

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            send_driver_notifications(self)


class DriverResponse(models.Model):
    STATUS_CHOICES = (
        ('a', 'Выбран пользователем'),
        ('n', ''),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    price = models.IntegerField(verbose_name='Стоимость', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан в")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n', verbose_name='Статус', null=True, blank=True)

    class Meta:
        verbose_name = ('Отклик на заказ')
        verbose_name_plural = ('Отклики на заказы')
        unique_together = ('order', 'driver')

    def __str__(self):
        return f"{self.order} - {self.driver}"

    def save(self, *args, **kwargs):
        created = not self.pk  # Check if the object is being created
        super().save(*args, **kwargs)
        if created:
            # Send email notification to the user
            user_email = self.order.client.email
            send_notification_email(user_email, self.order)


class OrderRating(models.Model):
    communication_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Коммуникация')
    driver_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Водитель')
    transport_rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],verbose_name='Транспорт')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')

    class Meta:
        verbose_name = ('Оценка заказа')
        verbose_name_plural = ('Оценки заказов')
        unique_together = ('order',)  # make order field unique

    def __str__(self):
        return f"Оценка №{self.id} от {self.order.created_at.strftime('%Y %m %d в %H:%M')}"


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

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name}. Оценка - {self.rating} ★"

    class Meta:
        verbose_name = ('Отзыв')
        verbose_name_plural = ('Отзывы')


class SupportRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'В ожидании'),
        ('ongoing', 'В работе'),
        ('resolved', 'Решен'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание проблемы")

    class Meta:
        verbose_name = ('Запрос в техподдержку')
        verbose_name_plural = ('Запросы в техподдержку')

    def __str__(self):
        return f"Запрос №{self.id} от {self.user.first_name} {self.user.last_name}."


@receiver(post_save, sender=User)
def create_driver(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        Driver.objects.create(user=instance, rating=4)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)