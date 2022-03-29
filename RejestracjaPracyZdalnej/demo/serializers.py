from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PracownikSerializer(serializers.HyperlinkedModelSerializer):
    firma = serializers.SlugRelatedField(queryset=Firma.objects.all(), slug_field='nazwaFirmy')


    class Meta:
        model = Pracownik
        fields = ['id', 'imie', 'nazwisko', 'pesel', 'firma', 'czyKierownik', 'czyAdministrator', 'login', 'mail', 'haslo']


class FirmaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Firma
        fields = ['id', 'nazwaFirmy']


class PracaSerializer(serializers.ModelSerializer):
    #idPracownika = serializers.SlugRelatedField(queryset=Pracownik.objects.all(), slug_field='idPracownika')
    class Meta:
        model = Praca
        fields = ['idPracownika','dataRozpoczecia', 'dataZakonczenia', 'minutyStart', 'minutyPozostalo', 'zlecajacy']