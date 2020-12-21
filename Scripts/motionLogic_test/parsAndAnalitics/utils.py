import re
import requests
from bs4 import BeautifulSoup as bs


payload = {
    'headers': {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
}


session = requests.session()

########     Parsing     ########
def get_McD_restaurants():
    """Возвращает список информации ресторанов Мака по России в json"""
    restaurants_json_list = []
    mcD_restaurants_map_url = 'https://mcdonalds.ru/restaurants/map'
    msD_restaurants_api = 'https://mcdonalds.ru/api/restaurant/'
    mcD_restaurants_page = session.get(mcD_restaurants_map_url, params=payload)
    soup = bs(mcD_restaurants_page.content, 'html.parser')
    script_having_restaurants = soup.find_all('script')
    restaurants_IDs = re.findall(r'id:(\w+),sort',str(script_having_restaurants[4])) # С помощью регулярных выражений собираем все id ресторанов
    for i in range(int(restaurants_IDs[-1])): # Некороторые рестораны имеют буквенный id, которые совпадают с id, равным порядковому значению ресторана.
        # По этому берём последний элемент (он числовой), переводим в int создаём из этого последовательность
        rest_json = session.get(msD_restaurants_api+f'{i + 1}').json()  # Получаем инфу ресторана по id ресторана
        if 'errors' in rest_json.keys():
            continue
        restaurants_json_list.append(rest_json)

    return get_restaurant_list_json('McD',restaurants_json_list)

def get_kfc_restaurants() -> list:
    """Возвращает список информации ресторанов КФЦ по России в json"""
    kfc_cities_coordinates_url = 'https://api.kfc.com/api/store/v2/store.get_cities'  # Post
    kfc_restaurants_url = 'https://api.kfc.com/api/store/v2/store.geo_search'  # Post
    restaurant_json_list = []
    restaurant_ids_list = []
    cities_info_list = session.post(kfc_cities_coordinates_url, params= payload).json()['value']['cities']
    cities_coordinates_list = []
    for city in cities_info_list:
        try:
            cities_coordinates_list.append(city['defaultStore']['coordinates']['geometry']['coordinates'])
        except:
            print(f'Не удалось получить координаты дефолтного магазина в городе {city["title"]["ru"]}')
            cities_coordinates_list.append([city["title"]["ru"]])
    for coordinates in cities_coordinates_list:
        try:
            data = ({
                'coordinates': [coordinates[0], coordinates[1]],
                'radiusMeters': 100000,
                'channel': "website"
            })
            kfc_restaurants_jsons = session.post(kfc_restaurants_url, json= data).json()['searchResults']
            for restaurant_json in kfc_restaurants_jsons:
                if restaurant_json['store']['storeId'] in restaurant_ids_list:
                    continue
                restaurant_json_list.append(restaurant_json)
                restaurant_ids_list.append(restaurant_json['store']['storeId'])
        except:
            restaurant_json_list.append({'city': f'{coordinates}'})

    return get_restaurant_list_json('KFC', restaurant_json_list)

def get_bk_restaurants():
    """Возвращает список информации ресторанов БК по России в json"""
    bk_cities_url = 'https://app.burgerking.ru/bridge/restaurants/search?is_active=true&geo=true'
    bk_cities_list_json = session.get(bk_cities_url).json()['response']
    return get_restaurant_list_json("BK", bk_cities_list_json)



def get_restaurant_list_json(corp: str, jsons: list):
    """Получает на вход название компании и список ресторанов компании в формате json,
    возваращает список словарей с нужной инфой для сохранения в модель"""
    restaurants_list = []
    c = corp.lower()
    if c == 'mcd':
        for j in jsons:
            try:
                city = f'{j["restaurant"]["location"]["name"]}'
            except:
                city = f'{j["restaurant"]["city"].split(" ")[-1]}'
            restaurants_list.append({
                'name_corp': f'{corp}',
                'name_in_corp_sys': f'{j["restaurant"]["name"]}',
                'city': f'{city}',
                'address': f'{j["restaurant"]["address"]}'
            })
    elif c == 'kfc':
        for j in jsons:
            if 'store' not in j.keys():
                continue
            try:
                city = f'{j["store"]["contacts"]["city"]["ru"]}'
                address = f'{j["store"]["contacts"]["streetAddress"]["ru"]}'
            except:
                city = f'{j["city"][0]}'
                address = f'{j["city"][0]}'
            if city.lower() == 'москва и мо':
                try:
                    city = re.findall(r'\d+, ([^,]*)', address)[0]
                except IndexError:
                    city = re.findall(r'([^,]*)', address)[0]
            restaurants_list.append({
                'name_corp': f'{corp}',
                'name_in_corp_sys': f'{j["store"]["title"]["ru"]}',
                'city': city,
                'address': address
            })


    elif c == 'bk':
        for j in jsons:
            city = re.findall(r"\W?(\w+[-\s]?\w*[-\s]?\w*)\s[гпдс][.]?,",j["address"])
            try:
                city = city[0]
            except:
                city = 'None'
            restaurants_list.append({
                'name_corp': f'{corp}',
                'name_in_corp_sys': f'{j["name"]}',
                'city': f'{city}',
                'address': f'{j["address"]}'
            })

    return restaurants_list



def main():
    pass

if __name__ == '__main__':
    main()