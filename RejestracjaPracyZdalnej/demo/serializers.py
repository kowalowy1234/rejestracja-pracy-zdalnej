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


class PracaSerializer(serializers.HyperlinkedModelSerializer):
    #login = serializers.SlugRelatedField(queryset=Pracownik.objects.all(), slug_field='login')
    class Meta:
        model = Praca
        fields = ['dataRozpoczecia', 'dataZakonczenia', 'minutyStart', 'minutyPozostalo', 'zlecajacy']