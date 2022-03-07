
from django.db import models


class Pracownik(models.Model):
    imie = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=45)
    pesel = models.CharField(max_length=45)
    czyKierownik = models.BooleanField()
    mail = models.CharField(max_length=45)
    haslo = models.CharField(max_length=45)

    def __str__(self):
        return self.imie + ' ' + self.nazwisko

    class Meta:
        verbose_name_plural = "Pracownicy"