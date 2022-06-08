from django.db.models import Sum, DateTimeField, DateField
from django.db.models.functions import Cast, TruncDate, TruncMonth, TruncWeek, TruncYear, TruncDay
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
from datetime import date
from dateutil.relativedelta import relativedelta
import json

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


class PrzepracowaneMinuty(generics.ListAPIView):
    serializer_class = StatystykiSerializer
    name = 'przepracowane-minuty'

    queryset = ZapisPracy.objects.all()
    filter_fields = {'created_at': ['iexact', 'lte', 'gte']}
    http_method_names = ['get', 'post', 'head']

    GROUP_BY = ["day", "week", "month", "year"]

    def obliczZakresDat(self, group_by_field):
        today = date.today()
        if group_by_field == "day":
            first_day = today - relativedelta(days=1)
            last_day = first_day
        elif group_by_field == "week":
            first_day = today - relativedelta(days=today.weekday(), weeks=1)
            last_day = today - relativedelta(days=today.weekday()) - relativedelta(days=1)
        elif group_by_field == "month":
            d = today - relativedelta(months=1)
            first_day = date(d.year, d.month, 1)  # pierwszy dzień z poprzedniego miesiąca
            last_day = date(today.year, today.month, 1) - relativedelta(days=1)  # ostatni dzień poprzedniego miesiąca
        elif group_by_field == "year":
            d = today - relativedelta(years=1)
            first_day = date(d.year, 1, 1)
            last_day = date(d.year, 12, 31)
        return first_day, last_day

    def list(self, request, *args, **kwargs):
        today = datetime.date.today()

        group_by_field = request.GET.get('group_by', None)

        if request.method == 'GET':
            data = json.loads(request.body)
            array = json.dumps(data)
            body = json.loads(array)
            body = body['ids']

            if(not body):
                return Response(status=status.HTTP_400_BAD_REQUEST)


        if group_by_field and group_by_field not in self.GROUP_BY:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if group_by_field:
            start, end = self.obliczZakresDat(group_by_field)
            final_data = []


            for x in body:
                queryset = ZapisPracy.objects.filter(
                    idPracownika=x,
                    data__gte=start,
                    data__lte=end
                ).values(
                    'idPracownika'
                ).annotate(
                    przepracowaneMinuty=Sum('przepracowaneMinuty')
                )

                query2 = User.objects.filter(id=x).values('first_name', 'last_name', 'email')

                if queryset:
                    slownik = queryset[0]
                    slownik["user"] = query2[0]
                    final_data.append(slownik)


            if final_data:
                return Response(final_data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
                         'statystykiUserList': "http://127.0.0.1:8000/auth/statystyki-user-list/1",
                         'przepracowaneMinutyDzien': "http://127.0.0.1:8000/auth/przepracowane-minuty/?group_by=day",
                         'przepracowaneMinutyTydzien': "http://127.0.0.1:8000/auth/przepracowane-minuty/?group_by=week",
                         'przepracowaneMinutyMiesiac': "http://127.0.0.1:8000/auth/przepracowane-minuty/?group_by=month",
                         'przepracowaneMinutyRok': "http://127.0.0.1:8000/auth/przepracowane-minuty/?group_by=year", })
