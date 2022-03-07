from django.urls import path, include
from . import views
from django.contrib import admin

admin.site.site_url = 'http://127.0.0.1:8000/demo/'
urlpatterns = [
    path('pracownik', views.PracownikList.as_view(), name='pracownik-list'),
    path('pracownikDetails', views.PracownikDetail.as_view(), name='pracownik-details'),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]