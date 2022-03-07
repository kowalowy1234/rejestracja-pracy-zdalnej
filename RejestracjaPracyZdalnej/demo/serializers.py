from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PracownikSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pracownik
        fields = ['id', 'imie', 'nazwisko', 'pesel', 'czyKierownik', 'mail', 'haslo']