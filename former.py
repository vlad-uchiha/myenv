import requests
import datetime
import json
import csv

# Чтение данных из файла и преобразование строк в словари
with open("cities_coordinates.json", 'r', encoding='utf-8') as file:
    cities_coords = json.load(file)

startTime = '2000-01-01'
endTime = '2020-01-01'
maxRadiusInKm = '75'
minMagnitude = '2.0'

# Функция для конвертации времени
def calculateTime(milliseconds):
    seconds = milliseconds / 1000
    dateOfEarthquake = datetime.datetime.fromtimestamp(seconds)
    return dateOfEarthquake

# Функция для получения данных о землетрясениях
def getData(startTime, endTime, cities_coords, maxradiuskm, minmagnitude):
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    earthquake_data = []  # Пустой список для хранения результатов

    for city in cities_coords:
        latitude = city['latitude']
        longitude = city['longitude']
        city_name = city['city']
        continent = city['Continent']

        response = requests.get(url, params={
            "format": "geojson",
            "starttime": startTime,
            "endtime": endTime,
            "latitude": latitude,
            "longitude": longitude,
            "maxradiuskm": maxradiuskm,
            "minmagnitude": minmagnitude
        })

        # Если данные найдены, добавляем их, иначе добавляем NULL
        if response.status_code == 200:
            try:
                data = response.json()
                if "features" in data and data["features"]:
                    for feature in data['features']:
                        timeKey = feature['properties']['time']
                        # Создаем словарь для каждого землетрясения
                        earthquake_dict = {
                            "City": city_name,
                            "Continent": continent,
                            "Place": feature['properties']['place'],                            
                            "Date": str(calculateTime(timeKey))[0:10],
                            "Time": str(calculateTime(timeKey))[11:19],
                            "Magnitude": feature['properties']['mag']
                        }
                        earthquake_data.append(earthquake_dict)
                else:
                    # Добавляем данные с NULL для городов без землетрясений
                    earthquake_data.append({
                        "City": city_name,
                        "Continent": "NULL",
                        "Place": "NULL",
                        "Date": "NULL",
                        "Time": "NULL",
                        "Magnitude": "NULL"
                    })
            except json.JSONDecodeError:
                print(f"Error decoding JSON for city {city_name}. Response text: {response.text}")
        else:
            print(f"Error: Received status code {response.status_code} for city {city_name}.")

    return earthquake_data

# Получаем данные о землетрясениях
earthquake_results = getData(startTime, endTime, cities_coords, maxRadiusInKm, minMagnitude)

    
#Сохраняем данные в CSV
with open("earthquake_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["City", "Continent", "Place", "Date", "Time", "Magnitude"])
    writer.writeheader()
    writer.writerows(earthquake_results)


print("Данные о землетрясениях сохранены в earthquake_data.csv")
