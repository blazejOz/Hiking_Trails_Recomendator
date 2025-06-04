from src.database.migration_tool import MigrationTool
from src.models.user_preference import UserPreference
from src.models.route import Route
from src.models.weather_data import WeatherData
from src.recommenders.route_recommender import RouteRecommender
from src.database.repositories.user_repository import UserRepository
from src.database.repositories.route_repository import RouteRepository
from src.database.repositories.weather_repository import WeatherRepository

def main_menu():
    while True:
        print("=== REKOMENDATOR TRAS TURYSTYCZNYCH ===")
        print("1. Znajdź rekomendowane trasy")
        print("2. Dodaj nową trasę")
        print("3. Statystyki bazy danych")
        print("4. Utwórz kopię zapasową")
        print("5. Importuj dane z CSV")
        print("0. Wyjście")

        choice = input("Wybierz opcję: ")
        if choice == '1':
            find_recommended_routes()
        elif choice == '2':
            add_new_route()
        elif choice == '3':
            show_database_statistics()
        elif choice == '4':
            pass
            #create_backup()
        elif choice == '5':
            print("Importowanie danych z pliku CSV...")
            routes = MigrationTool.migrate_routes()
            MigrationTool.migrate_weather_data(routes)
        elif choice == '0':
            print("Dziękujemy za skorzystanie z aplikacji!")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")

def find_recommended_routes():
    print("=== REKOMENDATOR TRAS TURYSTYCZNYCH ===")
    print("1. Nowe Wyszukiwanie")
    print("2. Wczytaj preferencje użytkownika")
    print("0. Powrót do menu głównego")

    choice = input("Wybierz opcję: ")
    if choice == '1':
        new_search()

def new_search():

    user_name = input("Podaj nazwę użytkownika: ")
    temp_min = float(input("Podaj minimalną preferowaną temperaturę (°C): "))
    temp_max = float(input("Podaj maksymalną preferowaną temperaturę (°C): "))
    max_precipitation = float(input("Podaj maksymalną ilość opadów (mm): "))
    max_difficulty = int(input("Podaj maksymalny poziom trudności (1-5): "))
    max_length = float(input("Podaj maksymalną długość trasy (km): "))

    new_user = UserPreference(
        user_name=user_name,
        preferred_temp_min=temp_min,
        preferred_temp_max=temp_max,
        max_precipitation=max_precipitation,
        max_difficulty=max_difficulty,
        max_length_km=max_length
    ) 

    routes = RouteRepository.get_all_routes()
    weather_data = WeatherRepository.get_all_weather_data()

    route_weather_pairs = RouteRecommender.recommend(routes, weather_data, new_user)    
    
    if not route_weather_pairs:
        print("Brak tras spełniających kryteria.")
    else:
        print_routes(route_weather_pairs)

def add_new_route():

    print("=== Dodaj nową trasę ===")
    name = input("Nazwa trasy: ")
    region = input("Region: ")
    start_lat = float(input("Szerokość geograficzna startu: "))
    start_lon = float(input("Długość geograficzna startu: "))
    end_lat = float(input("Szerokość geograficzna końca: "))
    end_lon = float(input("Długość geograficzna końca: "))
    elevation_gain = int(input("Przewyższenie (m): "))
    terrain_type = input("Typ terenu (forest, mountain, urban, lakeside): ")
    if terrain_type not in ["forest", "mountain", "urban", "lakeside"]:
        print("Nieprawidłowy typ terenu. Użyto domyślnego 'forrest'.")
        terrain_type = "forrest"
    length_km = float(input("Długość (km): "))
    difficulty = int(input("Trudność (1-5): "))
    tags = input("Tagi (oddzielone przecinkami): ").split(',')

    new_route = Route(
        id=None,  # ID will be assigned by the database
        name=name,
        region=region,
        start_lat=start_lat,
        start_lon=start_lon,
        end_lat=end_lat,
        end_lon=end_lon,
        length_km=length_km,
        elevation_gain=elevation_gain,
        difficulty=difficulty,
        terrain_type=terrain_type,
        tags=tags
    )
    RouteRepository.add_route(new_route)
    print(f"Trasa '{name}' została dodana pomyślnie.")

def show_database_statistics():
    print("=== Statystyki bazy danych ===")
    user_count = UserRepository.get_user_count()
    route_count = RouteRepository.get_route_count()
    weather_count = WeatherRepository.get_weather_data_count()

    print(f"Liczba użytkowników: {user_count}")
    print(f"Liczba tras: {route_count}")
    print(f"Liczba danych pogodowych: {weather_count}")

def print_routes(route_weather_pairs):
    print("\n=== Lista rekomendowanych tras ===")
    for route, weather in route_weather_pairs:
        print(f"{route.id}. {route.name}  ({route.region})")
        print(f"    Długość: {route.length_km} km")
        print(f"    Trudność: {route.difficulty}/5")
        print(f"    Szacowany czas: {route.estimated_completion()} h")
        print(f"    Komfort pogodowy: {weather.comfort_index()}")
        print(f"    Tagi: {', '.join(route.tags)}\n")

    