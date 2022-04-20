import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_random_string():
    length = 12
    letters = string.ascii_lowercase + string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class Firma(models.Model):
    nazwaFirmy = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.nazwaFirmy

    class Meta:
        verbose_name_plural = "Firmy"


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    phone = models.CharField(null=True, max_length=255)
    firma = models.ForeignKey(Firma, related_name='firma', on_delete=models.DO_NOTHING)
    pesel = models.CharField(max_length=11, unique=True)
    is_staff = models.BooleanField(null=True)
    is_superuser = models.BooleanField(null=True)
    REQUIRED_FIELDS = ['email', 'firma', 'is_staff', 'is_superuser', 'phone', 'first_name', 'last_name', 'pesel']
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username




class ZapisPracy(models.Model):
    idPracownika = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    przepracowaneMinuty = models.IntegerField()

    def __str__(self):
        return self.idPracownika

    class Meta:
        verbose_name_plural = "ZapisPrac"


class Praca(models.Model):
    idPracownika = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    dataRozpoczecia = models.DateTimeField(default=datetime.date.today())
    dataZakonczenia = models.DateTimeField(default=datetime.date.today())
    minutyStart = models.IntegerField(default=0)
    minutyPozostalo = models.IntegerField(default=0)
    zlecajacy = models.CharField(max_length=45, default=3)


    def __str__(self):
        return self.zlecajacy

    class Meta:
        verbose_name_plural = "Prace"


    @receiver(post_save, sender=User)
    def create_praca(instance, created, **kwargs):
        if created:
            Praca.objects.create(idPracownika=instance)