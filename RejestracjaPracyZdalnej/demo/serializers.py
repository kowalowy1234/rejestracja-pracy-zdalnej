from django.db.models import Count, Sum
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer

from django.contrib.auth import get_user_model

User = get_user_model()




class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'username', 'password',  'pesel',
                  'phone', 'firma']


class FirmaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Firma
        fields = ['id', 'nazwaFirmy']


class ZapisPracySerializer(serializers.ModelSerializer):
    class Meta:
        model = ZapisPracy
        fields = ['id', 'idPracownika', 'data', 'przepracowaneMinuty']


class PracaSerializer(serializers.ModelSerializer):
    # idPracownika = serializers.SlugRelatedField(queryset=Pracownik.objects.all(), slug_field='idPracownika')
    class Meta:
        model = Praca
        fields = ['idPracownika', 'dataRozpoczecia', 'dataZakonczenia', 'minutyStart', 'minutyPozostalo', 'zlecajacy']


class StatystykiSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZapisPracy
        fields = ['id', 'idPracownika', 'data', 'przepracowaneMinuty']