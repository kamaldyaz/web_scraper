import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from tabulate import tabulate
import json

def get_forecast_data():
    url = 'https://world-weather.info/'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36', 'cookie': 'celsius = 1'}

    response = requests.get(url, headers=headers)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        resorts = soup.find('div', id='resorts')

        re_cities = r'">([\w\s]+)<\/a><span>'
        cities = re.findall(re_cities, str(resorts))

        re_temps = r'<span>(\+\d+|-\d+)<span'
        temps = re.findall(re_temps, str(resorts))
        temps = [int(temp) for temp in temps]

        conditions_tags = resorts.find_all('span', class_='tooltip')
        conditions = [condition.get('title') for condition in conditions_tags]

        data = zip(cities, temps, conditions)

        return data

    return False

def get_forecast_txt():
    data = get_forecast_data()

    if  data:
        today = date.today().strftime('%d/%m/%Y')
        with open('output.txt', 'w') as f:
            f.write('Popular Cities Forecast' + '\n')
            f.write(today + '\n')
            f.write('='*23 + '\n')
            table = tabulate(data, headers=['city', 'temp.', 'condition'], tablefmt='grid')
            f.write(table)

def get_forecast_json():
    data = get_forecast_data()

    if data:
        today = date.today().strftime('%d/%m/%Y')

        cities = [{'city': city, 'temp': temp, 'condition': condition} for city, temp, condition in data]
        data_json = {'title': 'Popular Cities Forecast', 'date': today, 'cities': cities}

        with open('output.json', 'w') as f:
            json.dump(data_json, f, ensure_ascii=False)



if __name__ == '__main__':
    get_forecast_txt()
    get_forecast_json()