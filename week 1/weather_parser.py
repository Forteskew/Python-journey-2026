import requests
import json
from datetime import datetime

def get_weather(city):
    """Получает текущую погоду для города"""
    # здесь будет код запроса
    url = "https://api.open-meteo.com/v1/forecast?latitude=55.75&longitude=37.62&current_weather=true&timezone=Europe%2FMoscow"

    response = requests.get(url)            # отправляем запрос

    if response.status_code == 200:         # 200 - все хорошо
        data = response.json()
        return data
    else:
        return f"Ошбика: {response.status_code}"
    
def get_coordinates(city):
    """Находит координаты города по его названию"""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=ru"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
def get_weather_by_city(city):
    """Полная функция: находит координаты города и получает погоду"""
    
    # 1. Ищем координаты города
    coord_data = get_coordinates(city)
    
    if coord_data is None:
        print(f"❌ Не удалось подключиться к сервису поиска городов.")
        return None
    
    if "results" not in coord_data or len(coord_data["results"]) == 0:
        print(f"❌ Город '{city}' не найден. Попробуйте написать название по-другому.")
        return None
    
    # Берём первый (самый подходящий) результат
    result = coord_data["results"][0]
    latitude = result["latitude"]
    longitude = result["longitude"]
    found_city = result.get("name", city)
    country = result.get("country", "")
    
    print(f"📍 Найден: {found_city}, {country} ({latitude}, {longitude})")
    
    # 2. Получаем погоду по координатам
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    
    response = requests.get(url)
    
    if response.status_code == 200:
                # Сохраняем запрос в историю
        history = load_history()
        
        history.append({
            "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "city": found_city,
            "country": country,
            "temperature": current.get("temperature") if 'current' in locals() else None
        })
        
        save_history(history)

        return response.json()
    else:
        print(f"❌ Ошибка при получении погоды: {response.status_code}")
        return None
    
def show_weather(data):
    """Красиво показывает информацию о погоде + рекомендацию"""
    
    # Проверка 1: данные вообще пришли?
    if data is None or isinstance(data, str):   # если пришло сообщение об ошибке
        print("❌ Не удалось получить данные о погоде.")
        print(data)  # покажем, что именно пошло не так
        return
    
    # Проверка 2: есть ли нужный ключ?
    if "current_weather" not in data:
        print("❌ Данные пришли, но формат не тот, как ожидалось.")
        return
    
    current = data["current_weather"]
    
    temperature = current.get("temperature")
    windspeed = current.get("windspeed")
    winddirection = current.get("winddirection")
    weather_time = current.get("time")
    
    # Вывод основных данных
    print(f"🌡️  Температура: {temperature} °C")
    print(f"🌬️  Скорость ветра: {windspeed} km/h")
    print(f"🧭  Направление ветра: {winddirection}°")
    
    # Рекомендация
    print("\nРекомендация:")
    if temperature is None:
        print("Не удалось определить температуру.")
    elif temperature > 15:
        print("☀️  Тепло. Можно в лёгкой одежде.")
    elif temperature > 5:
        print("🧥  Прохладно. Надень куртку.")
    elif temperature > 0:
        print("🥶  Холодно. Шапка и шарф обязательны.")
    else:
        print("❄️  Мороз! Одевайся максимально тепло.")
    
    if windspeed and windspeed > 20:
        print("💨  Сильный ветер, будь осторожен!")
    
    # Красивое время
    if weather_time:
        try:
            dt = datetime.fromisoformat(weather_time.replace("T", " "))
            formatted_time = dt.strftime("%d.%m.%Y %H:%M")
            print(f"\n🕒 Погода актуальна на: {formatted_time}")
        except:
            print(f"\n🕒 Время: {weather_time}")

def load_history():
    """Загружает историю запросов из файла"""
    try:
        with open("weather_history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_history(history):
    """Сохраняет историю запросов в файл"""
    with open("weather_history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

print("🌤️ Простой парсер погоды")

while True:
    city = input("\nВведите название города (или 'выход' для завершения): ").strip()
    
    if city.lower() == "выход":
        print("До свидания!")
        break
    
    # Пока просто выводим, что ввёл пользователь
    print(f"Вы ввели город: {city}")
    weather_data = get_weather_by_city(city)
    show_weather(weather_data)

        # Сохранение истории (простой вариант)
    history = load_history()
    history.append({
            "timestamp": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "city": city
        })
    save_history(history)

    

