from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Driver


@receiver(post_save, sender=User)
def create_driver(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        driver = Driver.objects.create(user=instance)
        driver.save()


post_save.connect(create_driver, sender=User)
