import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote

def get_city_coordinates(city_name):
    # Формируем URL страницы Википедии для конкретного города с кодированием символов
    url = f"https://en.wikipedia.org/wiki/{quote(city_name)}"
    response = requests.get(url)

    # Проверка успешности запроса
    if response.status_code != 200:
        print(f"Ошибка: не удалось получить данные для города {city_name} (HTTP {response.status_code})")
        return None

    # Парсим HTML контент страницы
    soup = BeautifulSoup(response.text, "html.parser")

    # Ищем элемент, содержащий координаты
    geo = soup.find("span", {"class": "geo"})
    if geo:
        # Извлекаем текст и разделяем его на широту и долготу
        lat, lon = geo.text.split("; ")
        # Преобразуем широту и долготу в формат с двумя знаками после запятой
        return {
            "city": city_name,
            "latitude": round(float(lat), 2),
            "longitude": round(float(lon), 2)
        }
    else:
        print(f"Координаты для города {city_name} не найдены.")
        return None

# Список городов для парсинга
cities = [
    "Washington, D.C.", "Mexico City", "New York City", "Toronto", "Havana", "Santo Domingo", "San Salvador", "San Antonio", "Dallas", "Montreal", 
    "Lagos", "Kinshasa", "Cairo", "Luanda", "Abidjan", "Alexandria", "Dar es Salaam", "Johannesburg", "Giza", "Nairobi",
    "Sao Paulo", "Lima", "Bogota", "Rio de Janeiro", "Santiago", "Caracas", "Buenos Aires", "Brasília", "Fortaleza", 
    "Istanbul", "Moscow", "London","Saint Petersburg", "Berlin", "Madrid", "Kyiv", "Rome", "Baku", "Paris",
    "Guangzhou", "Jakarta", "Mumbai", "Delhi", "Tokyo", "Shanghai", "Manila", "Seoul", "Dhaka", "Beijing"
]

# Парсинг координат для каждого города
city_coordinates = []
for city in cities:
    coordinates = get_city_coordinates(city)
    if coordinates:
        city_coordinates.append(coordinates)

for i, record in enumerate(city_coordinates):
    if 0 <= i < 10:
        record['Continent'] = "North America"
    elif 10 <= i < 20:
        record['Continent'] = "Africa"
    elif 20 <= i < 29:
        record['Continent'] = "South America"
    elif 29 <= i < 39:
        record["Continent"] = "Europe"
    elif 39 <= i < 49:
        record["Continent"] = "Asia"

#Сохранение данных в JSON для удобного чтения
with open("cities_coordinates.json", "w", encoding="utf-8") as file:
    json.dump(city_coordinates, file, ensure_ascii=False, indent=4)

print("Координаты успешно сохранены в файл cities_coordinates.json")
