from django.db import models
import random
import string


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


class Pracownik(models.Model):
    imie = models.CharField(max_length=45)
    nazwisko = models.CharField(max_length=45)
    pesel = models.CharField(max_length=11, unique=True)
    firma = models.ForeignKey(Firma, related_name='firma', on_delete=models.DO_NOTHING, default=3)
    czyKierownik = models.BooleanField(default=False)
    czyAdministrator = models.BooleanField(default=False)
    mail = models.CharField(max_length=45)
    haslo = models.CharField(max_length=12, default=get_random_string())
    login = models.CharField(max_length=20)

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

    # login = property(_generatelogin)

    def __str__(self):
        return self.imie + ' ' + self.nazwisko

    class Meta:
        verbose_name_plural = "Pracownicy"


class ZapisPracy(models.Model):
    idPracownika = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    data = models.DateTimeField()
    przepracowaneMinuty = models.IntegerField()

    def __str__(self):
        return self.idPracownika

    class Meta:
        verbose_name_plural = "ZapisPrac"

class Praca(models.Model):
    idPracownika = models.ForeignKey(Pracownik, null=True, on_delete=models.SET_NULL)
    dataRozpoczecia = models.DateTimeField()
    dataZakonczenia = models.DateTimeField()
    minutyStart = models.IntegerField()
    minutyPozostalo = models.IntegerField()
    zlecajacy = models.CharField(max_length=45)

    def __str__(self):
        return self.zlecajacy

    class Meta:
        verbose_name_plural = "Prace"


