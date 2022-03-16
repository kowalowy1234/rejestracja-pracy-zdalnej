from django.db import models
import random
import string


def get_random_string():
    length = 12
    letters = string.ascii_lowercase + string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class Pracownik(models.Model):
    imie = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=45)
    pesel = models.CharField(max_length=11, unique=True)
    czyKierownik = models.BooleanField(default=False)
    czyAdministrator = models.BooleanField(default=False)
    mail = models.CharField(max_length=45)
    haslo = models.CharField(max_length=12, default=get_random_string())

    def _peselRandom(self):
        peselChars = [char for char in str(self.pesel)]
        randomPesel = ''
        for i in range(4):
            randomPesel += str(peselChars[random.randint(0, len(peselChars) - 1)])
        return randomPesel

    def _generatelogin(self):
        imie = str(self.imie)
        nazwisko = str(self.nazwisko)
        result = '' + imie[0] + nazwisko + self._peselRandom()

        return str(result)

    login = property(_generatelogin)

    def __str__(self):
        return self.imie + ' ' + self.nazwisko

    class Meta:
        verbose_name_plural = "Pracownicy"
