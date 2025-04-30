import csv
import requests

### OBSŁUGA DANYCH ###
def load_trails(filePath):
    '''
        ladowanie tras z pliku csv(gotowego)
    '''

    trails = []
    with open(filePath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            trails.append(row)
    return trails

def get_weather(lat, lon):
    '''
        pobieranie danych pogodowych z open meteo
        url zawiera info o lat i long oraz ile dni w przod prognoza (7)
    '''
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,precipitation_sum,cloudcover_mean&forecast_days=7&timezone=Europe%2FWarsaw"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['daily']
    else:
        print("Error fetching weather data")
        return None
    
def save_recomended_trails(recommendations, filename="recomended_trails.csv"):
    fieldnames = list(recommendations[0].keys())

    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(recommendations)
    
    print(f"Zapisano {len(recommendations)} tras do pliku '{filename}'")

def save_wather_data(weather_data, filename="weather_info.csv"):
    fieldnames = weather_data[0].keys()
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(weather_data)
    print(f"Zapisano {len(weather_data)} informacji pogodowych do pliku '{filename}'")
    
### ANALIZA DANYCH ###
def recomend_trails(trails, preferred_length,  preferred_terrain, preferred_difficulty):
    filtered = filter(
        lambda x: (
            int(x["difficulty"]) <= preferred_difficulty
            and preferred_terrain in x["terrain_type"].lower()
            and float(x["length_km"]) <= preferred_length
        ),
        trails
    )

    recommended = list(filtered)
    return recommended

def get_weather_for_trails(recommended):
    weather_info = []

    for trail in recommended:
        lat = float(trail["start_lat"])
        lon = float(trail["start_lon"])
        weather = get_weather(lat, lon) 

        if weather:
            temps = weather["temperature_2m_max"][:7]
            rain = weather["precipitation_sum"][:7]
            clouds = weather["cloudcover_mean"][:7]

            avg_temp = sum(temps) / len(temps)
            total_rain = sum(rain)
            sunny_days = sum(1 for c in clouds if c < 30)

            weather_info.append({
                "name": trail["name"],
                "region": trail["region"],
                "avg_temp": round(avg_temp, 1),
                "total_rain": round(total_rain, 1),
                "sunny_days": sunny_days
            })

    
    return weather_info

def print_trails(trails):
    print("\n=== Lista Tras ===")
    for trail in trails:
        print(f"{trail['id']}. {trail['name']} - {trail['region']} | {trail['length_km']} km | "
              f"trudność: {trail['difficulty']} | teren: {trail['terrain_type']}")

def print_weather_info(weather_info):
    print("\n=== Pogoda dla rekomendowanych tras (kolejne 7 dni) ===")
    for w in weather_info:
        print(f"{w['name']} → {w['region']} | Śr. temp: {w['avg_temp']}°C | "
              f"Opady: {w['total_rain']} mm | Słoneczne dni: {w['sunny_days']}")

### INTERFEJS UZYTKOWNIKA ###
def userUI():

    trails = load_trails("trasy.csv")

    print("=== Preferencje użytkownika ===")
    preferred_length = float(input("Maksymalna długość trasy (km): "))
    preferred_terrain = input("Preferowany typ terenu (np. mountain, lakeside, forest): ").strip().lower()
    preferred_difficulty = int(input("Maksymalny poziom trudności (1 = łatwy, 3 = trudny): "))

    recommended_trails = recomend_trails(trails, preferred_length, preferred_terrain, preferred_difficulty)
    print_trails(recommended_trails)

    trail_weather = get_weather_for_trails(recommended_trails)
    print_weather_info(trail_weather)

    save_recomended_trails(recommended_trails)
    save_wather_data(trail_weather)



userUI()

