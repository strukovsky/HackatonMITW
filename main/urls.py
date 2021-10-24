from django.contrib import admin
from django.urls import path

from main import views

urlpatterns = [
    path('change_order', views.change_order), #
    path('', views.index),
    path('prepare', views.prepare),
    path('concat', views.concat), #
    path('clear', views.clear),
    path('storage', views.storage),
    path('split', views.split), #
    path('rotate', views.rotate), #
    path('archive', views.archive), #
    path('remove_pages', views.remove_pages),
    path('rotate_pages', views.rotate_pages), #
    path('view_doc', views.view_doc), #
    path('test', views.test),



]
