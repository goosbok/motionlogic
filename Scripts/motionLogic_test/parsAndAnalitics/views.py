from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurants
from .utils import *
import pandas as pnd

def index(request):
    return render(request, 'parsAndAnalitics/index.html')

def data(request):
    qs = Restaurants.objects.all()
    count_restaurants_BK = len(qs.filter(name_corp= 'BK'))
    count_restaurants_KFC = len(qs.filter(name_corp= 'KFC'))
    count_restaurants_McD = len(qs.filter(name_corp= 'McD'))
    content = {
        'counts': {
            'BK': count_restaurants_BK,
            'KFC': count_restaurants_KFC,
            'McD': count_restaurants_McD,
        }
    }
    return render(request, 'parsAndAnalitics/data_info.html', context= content)


def loader(request):
    restaurants_lists = [
        get_bk_restaurants(),
        get_kfc_restaurants(),
        get_McD_restaurants()
    ]

    for restaurants_list in restaurants_lists:
        for restaurant in restaurants_list:
            Restaurants.objects.create(
                name_corp= restaurant['name_corp'],
                name_in_corp_sys= str(restaurant['name_in_corp_sys']),
                city= str(restaurant['city']),
                address= str(restaurant['address'])
            )

    return HttpResponse(f'<h1>Выполнено</h1><p>Загружено {len(Restaurants.objects.all())} ресторанов</p>')

def get_table(request, name_corp):
    qs = Restaurants.objects.filter(name_corp= name_corp).values()
    table = pnd.DataFrame(qs).to_html()
    return render(request, 'parsAndAnalitics/table.html', context={'table': table})

def get_analitics(request):
    qs = Restaurants.objects.filter(city= 'Москва')
    context = {
    'all_restaurants_in_Msc': len(qs),
    'bk_restaurants_in_Msc': len(qs.filter(name_corp= 'BK')),
    'kfc_restaurants_in_Msc': len(qs.filter(name_corp= 'KFC')),
    'mcd_restaurants_in_Msc': len(qs.filter(name_corp= 'McD')),
    'bk_all': round(len(qs.filter(name_corp= 'BK'))/len(qs)*100),
    'kfc_all': round(len(qs.filter(name_corp= 'KFC'))/len(qs)*100),
    'mcd_all': round(len(qs.filter(name_corp= 'McD'))/len(qs)*100),
    }

    return render(request, 'parsAndAnalitics/analitics.html', context=context)