from django.urls import path, include
from . import views
from django.contrib import admin

admin.site.site_url = 'http://127.0.0.1:8000/demo/'
urlpatterns = [
    path('firma', views.FirmaList.as_view(), name='firma-list'),
    path('firma/<int:pk>', views.FirmaDetail.as_view(), name='firma-details'),
    path('zapis-pracy', views.ZapisPracyList.as_view(), name='zapis-pracy-list'),
    path('zapis-pracy/<int:pk>', views.ZapisPracyDetail.as_view(), name='zapis-pracy-details'),
    path('praca', views.PracaList.as_view(), name='praca-list'),
    path('praca/<int:pk>', views.PracaDetail.as_view(), name='praca-details'),
    path('user', views.UserList.as_view(), name='user-list'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='user-details'),
    path('statystyki', views.StatystykiList.as_view(), name='statystyki'),
    path('statystyki-user/<int:pk>', views.StatystykiUser.as_view(), name='statystyki-user'),
    path('statystyki-user-list/<int:pk>', views.StatystykiUserList.as_view(), name='statystyki-user-list'),
    path('przepracowane-minuty/<int:pk>/', views.PrzepracowaneMinuty.as_view(), name='przepracowane-minuty'),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]