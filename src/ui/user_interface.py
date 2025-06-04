from src.database.migration_tool import MigrationTool


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
            pass
            #add_new_route()
        elif choice == '3':
            pass
            #show_database_statistics()
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
    from src.models.user_preference import UserPreference
    from src.database.repositories.user_repository import UserRepository
    from src.database.repositories.route_repository import RouteRepository
    from src.database.repositories.weather_repository import WeatherRepository

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
    UserRepository.add_user_preference(new_user)

    routes = RouteRepository.get_all_routes()
    weather_data = WeatherRepository.get_all_weather_data()

    route_weather_pairs = []
    
    for route in routes:
        if new_user.matches_route(route):
            for weather in weather_data:
                if new_user.matches_weather(weather):
                    route_weather_pairs.append((route, weather))

    if not route_weather_pairs:
        print("Brak tras spełniających kryteria.")
    else:
        print_routes(route_weather_pairs)


def print_routes(route_weather_pairs):
    print("\n=== Lista rekomendowanych tras ===")
    for route, weather in route_weather_pairs:
        print(f"{route.id}. {route.name}  ({route.region})")
        print(f"    Długość: {route.length_km} km")
        print(f"    Trudność: {route.difficulty}/3")
        print(f"    Szacowany czas: {route.estimated_completion()} h")
        print(f"    Komfort pogodowy: {weather.comfort_index()}")
        print(f"    Tagi: {', '.join(route.tags)}\n")

    