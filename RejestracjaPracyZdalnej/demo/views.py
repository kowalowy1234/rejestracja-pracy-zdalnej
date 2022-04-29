from django.db.models import Sum
from django.shortcuts import render
from rest_framework.exceptions import NotFound

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



class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    name = 'user-details'


class StatystykiList(generics.ListAPIView):
    serializer_class = StatystykiSerializer
    name = 'statystyki'
    queryset = ZapisPracy.objects.all()

    def list(self, request, *args, **kwargs):
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)

        queryset = ZapisPracy.objects.filter(
            data__gte=thirty_days_ago
        ).values(
            'idPracownika'
        ).annotate(
            przepracowaneMinuty=Sum('przepracowaneMinuty')
        ).order_by('idPracownika')

        if queryset:
            return Response(queryset)
        else:
            raise NotFound()


class StatystykiUser(generics.ListAPIView):
    serializer_class = StatystykiSerializer
    name = 'statystyki-details'

    def list(self, request, *args, **kwargs):
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)
        slug = self.kwargs['pk']

        queryset = ZapisPracy.objects.filter(
            idPracownika=slug,
            data__gte=thirty_days_ago
        ).values(
            'idPracownika'
        ).annotate(
            przepracowaneMinuty=Sum('przepracowaneMinuty')
        )

        if queryset:
            return Response(queryset)
        else:
            raise NotFound()


class StatystykiUserList(generics.ListAPIView):
    serializer_class = StatystykiSerializer

    def get_queryset(self):
        slug = self.kwargs['pk']
        queryset = ZapisPracy.objects.filter(idPracownika=slug)
        if queryset:
            return queryset
        else:
            raise NotFound()


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({'pracownicy': reverse(UserList.name, request=request),
                         'firmy': reverse(FirmaList.name, request=request),
                         'zapisy pracy': reverse(ZapisPracyList.name, request=request),
                         'prace': reverse(PracaList.name, request=request),
                         'edycjaPracy': "http://127.0.0.1:8000/auth/praca/1",
                         'statystyki': "http://127.0.0.1:8000/auth/statystyki",
                         'statystykiUser': "http://127.0.0.1:8000/auth/statystyki-user/1",
                         'statystykiUserList': "http://127.0.0.1:8000/auth/statystyki-user-list/1", })