import json

files = [
    'restaurantsKFC.json',
    'restaurantsMcD.json',
    'restaurantsBK.json',
]

def load_jsons_to_model():
    for file in files:
        with open(file, 'r') as f:
            restaurants_json = json.load(f)
        for restaurant in restaurants_json:
            Restaurants.objects.create(
                name_corp= restaurant['name_corp'],
                name_in_corp_sys= restaurant['name_in_corp_sys'],
                city= restaurant['city'],
                address= restaurant['address']
            )
    return Restaurants.objects.all()


def main():
    print(load_jsons_to_model())

if __name__ == '__main__':
    main()
