from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('', views.index),
    path('prepare', views.prepare),
    path('concat', views.concat),
    path('clear', views.clear),
    path('storage', views.storage),
    path('split', views.split),

]
