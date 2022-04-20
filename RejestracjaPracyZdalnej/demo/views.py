from django.shortcuts import render
from django.views.generic import UpdateView

from .models import *
from .serializers import *
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

class PracownikList(generics.ListCreateAPIView):
    queryset = Pracownik.objects.all()
    serializer_class = PracownikSerializer
    name = 'pracownik-list'


class PracownikDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pracownik.objects.all()
    serializer_class = PracownikSerializer
    name = 'pracownik-details'

class FirmaList(generics.ListCreateAPIView):
    queryset = Firma.objects.all()
    serializer_class = FirmaSerializer
    name = 'firma-list'


class FirmaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Firma.objects.all()
    serializer_class = FirmaSerializer
    name = 'firma-details'


class ZapisPracyList(generics.ListCreateAPIView):
    queryset = ZapisPracy.objects.all()
    serializer_class = ZapisPracySerializer
    name = 'zapis-pracy-list'


class ZapisPracyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ZapisPracy.objects.all()
    serializer_class = ZapisPracySerializer
    name = 'zapis-pracy-details'


class PracaList(generics.ListCreateAPIView):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
    name = 'praca-list'


class PracaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
    name = 'praca-details'


class PracaUpdateView(UpdateView):
    model = Praca
    fields = [ "dataRozpoczecia",
               "dataZakonczenia",
               "minutyStart",
               "minutyPozostalo"]

    success_url = "/"


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'user-details'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'pracownicy': reverse(UserList.name, request=request),
                         'firmy': reverse(FirmaList.name, request=request),
                         'zapisy pracy': reverse(ZapisPracyList.name, request=request),
                         'prace': reverse(PracaList.name, request=request),})
