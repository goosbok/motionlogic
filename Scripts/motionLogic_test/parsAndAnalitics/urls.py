from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('data/', data, name='data_url'),
    path('pars/', loader, name='pars_url'),
    path('table/<str:name_corp>/', get_table, name='table_url'),
    path('analitics/', get_analitics, name='analitics_url'),
]