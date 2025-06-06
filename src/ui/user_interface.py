from datetime import date, datetime
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.database.database_manager import DatabaseManager
from src.database.migration_tool import MigrationTool
from src.models.user_preference import UserPreference
from src.models.route import Route
from src.models.weather_data import WeatherData
from src.recommenders.route_recommender import RouteRecommender
from src.database.repositories.user_repository import UserRepository
from src.database.repositories.route_repository import RouteRepository
from src.database.repositories.weather_repository import WeatherRepository
from src.reporters.pdf_report_generator import PDFReportGenerator

def main_menu():
    while True:
        print("=== REKOMENDATOR TRAS TURYSTYCZNYCH ===")
        print("1. Znajdź rekomendowane trasy")
        print("2. Dodaj nową trasę")
        print("3. Statystyki bazy danych")
        print("4. Utwórz/Wczytaj kopię zapasową")
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
            backup()
        elif choice == '5':
            import_csv()
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
    elif choice == '2':
        load_user_preferences()
    elif choice == '0':
        print("Powrót do menu głównego.")
        main_menu()
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
        find_recommended_routes()

def new_search():
    print()
    print("=== Nowe Wyszukiwanie ===")
    temp_min_input = input("Podaj minimalną preferowaną temperaturę (°C): ")
    temp_min = float(temp_min_input) if temp_min_input else 10.0

    temp_max_input = input("Podaj maksymalną preferowaną temperaturę (°C): ")
    temp_max = float(temp_max_input) if temp_max_input else 30.0

    max_precipitation_input = input("Podaj maksymalną ilość opadów (mm): ")
    max_precipitation = float(max_precipitation_input) if max_precipitation_input else 10.0

    max_difficulty_input = input("Podaj maksymalny poziom trudności (1-5): ")
    max_difficulty = int(max_difficulty_input) if max_difficulty_input else 3

    max_length_input = input("Podaj maksymalną długość trasy (km): ")
    max_length = float(max_length_input) if max_length_input else 20.0

    # Ask for MM-DD and build a date string with the current year
    mmdd = input("Podaj datę prognozy (MM-DD): ")
    if mmdd:
        current_year = datetime.now().year
        searched_forecast_date = f"{current_year}-{mmdd}"
    else:
        searched_forecast_date = date.today()

    new_user = UserPreference(
        id=None,  # ID will be assigned by the database
        user_name='default',
        preferred_temp_min=temp_min,
        preferred_temp_max=temp_max,
        max_precipitation=max_precipitation,
        max_difficulty=max_difficulty,
        max_length_km=max_length,
        forecast_date=searched_forecast_date)
    
    search_routes(new_user)
    
def load_user_preferences():
    print()
    print("=== Wczytaj preferencje użytkownika ===")
    user_name = input("Podaj nazwę użytkownika: ") or 'default'
    if UserRepository.check_user_exists(user_name):
        print(f"Wczytywanie preferencji użytkownika '{user_name}'...")
        user = UserRepository.get_user_preference(user_name)
    else:
        print(f"Użytkownik '{user_name}' nie istnieje.")
        print("1. Spróbuj ponownie")
        print("2. Utwórz nowego użytkownika")
        print("0. Powrót do menu głównego")
        choice = input("Wybierz opcję: ")
        if choice == '1':
            load_user_preferences()
        elif choice == '2':
            new_search()
        elif choice == '0':
            print("Powrót do menu głównego.")
            main_menu()
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")
            load_user_preferences()

    search_routes(user)

def search_routes(user):
    print()
    print("=== Wyszukiwanie tras ===")
    route_weather_pairs = RouteRecommender.recommend(user)

    if not route_weather_pairs:
        print("Brak tras spełniających kryteria.")
    else:
        print_routes(route_weather_pairs)

    end_search(route_weather_pairs, user)

def end_search(route_weather_pairs, user):
    print("=== KONIEC REKOMENDACJI ===")
    print("1. Nowe Wyszukiwanie")
    print("2. Zapisz preferencje użytkownika")
    print("3. Raport PDF")
    print("0. Powrót do menu głównego")

    choice = input("Wybierz opcję: ")
    if choice == '1':
        new_search()
    elif choice == '2':
        save_user_preferences(user)
        print("Preferencje zapisane.")
    elif choice == '3':
        print("Generowanie raportu PDF...")
        routes = [pair[0] for pair in route_weather_pairs]
        weather_data = [pair[1] for pair in route_weather_pairs]
        pdgreport = PDFReportGenerator(routes, weather_data , user)
        pdgreport.generate(f"raport_rekomendacji_{user.name}.pdf")
        print("Raport PDF został wygenerowany.")
    elif choice == '0':
        print("Powrót do menu głównego.")
        main_menu()
        return
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
        end_search(route_weather_pairs, user)

def save_user_preferences(new_user):
    print()
    print("=== Zapisz preferencje użytkownika ===")
    user_name = input("Nazwa użytkownika (lub pozostaw puste dla domyślnej): ")
    new_user.name = user_name if user_name else 'default'

    if UserRepository.check_user_exists(new_user.name):
        UserRepository.update_user_preference(new_user)
        print("Użytkownik istnieje, aktualizowanie preferencji...")
        print(f"Preferencje użytkownika '{new_user.name}' zostały zaktualizowane.")
    else:
        UserRepository.add_user_preference(new_user)
        print(f"Preferencje użytkownika '{new_user.name}' zostały zapisane.")

def add_new_route():
    print()
    print("=== Dodaj nową trasę ===")
    name = input("Nazwa trasy: ").strip()
    region = input("Region: ").strip()

    # Walidacja współrzędnych
    while True:
        try:
            start_lat = float(input("Szerokość geograficzna startu (-90 do 90): "))
            if not -90 <= start_lat <= 90:
                raise ValueError
            break
        except ValueError:
            print("Podaj poprawną szerokość geograficzną (-90 do 90).")

    while True:
        try:
            start_lon = float(input("Długość geograficzna startu (-180 do 180): "))
            if not -180 <= start_lon <= 180:
                raise ValueError
            break
        except ValueError:
            print("Podaj poprawną długość geograficzną (-180 do 180).")

    while True:
        try:
            end_lat = float(input("Szerokość geograficzna końca (-90 do 90): "))
            if not -90 <= end_lat <= 90:
                raise ValueError
            break
        except ValueError:
            print("Podaj poprawną szerokość geograficzną (-90 do 90).")

    while True:
        try:
            end_lon = float(input("Długość geograficzna końca (-180 do 180): "))
            if not -180 <= end_lon <= 180:
                raise ValueError
            break
        except ValueError:
            print("Podaj poprawną długość geograficzną (-180 do 180).")

    while True:
        try:
            elevation_gain = int(input("Przewyższenie (m, >=0): "))
            if elevation_gain < 0:
                raise ValueError
            break
        except ValueError:
            print("Podaj nieujemną liczbę całkowitą.")

    # Typ terenu
    valid_terrain = ["forest", "mountain", "urban", "lakeside"]
    terrain_type = input(f"Typ terenu {valid_terrain}: ").strip().lower()
    if terrain_type not in valid_terrain:
        print(f"Nieprawidłowy typ terenu. Użyto domyślnego '{valid_terrain[0]}'.")
        terrain_type = valid_terrain[0]

    while True:
        try:
            length_km = float(input("Długość (km, >0): "))
            if length_km <= 0:
                raise ValueError
            break
        except ValueError:
            print("Podaj dodatnią liczbę.")

    while True:
        try:
            difficulty = int(input("Trudność (1-5): "))
            if not 1 <= difficulty <= 5:
                raise ValueError
            break
        except ValueError:
            print("Podaj liczbę od 1 do 5.")

    tags = [tag.strip() for tag in input("Tagi (oddzielone przecinkami): ").split(',') if tag.strip()]

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

def backup():
    print("=== backup manager ===")
    print("1. Utwórz kopię zapasową bazy danych")
    print("2. Przywróć bazę danych z kopii zapasowej")
    print("0. Powrót do menu głównego")

    choice = input("Wybierz opcję: ")
    if choice == '1':
        backup_path = DatabaseManager.create_backup()
        print(f"Kopia zapasowa została utworzona: {backup_path}")
    elif choice == '2':
        backup_filename = input("Podaj nazwę pliku kopii zapasowej (np. db_backup_YYYYMMDD.sqlite3): ")
        try:
            restored_path = DatabaseManager.restore_database(backup_filename)
            print(f"Baza danych została przywrócona z: {restored_path}")
        except FileNotFoundError as e:
            print(e)
    elif choice == '0':
        print("Powrót do menu głównego.")
        main_menu()
    else:
        print("Nieprawidłowy wybór, spróbuj ponownie.")
        backup()
    
def import_csv():
    print("Importowanie danych z pliku CSV...")
    routes = MigrationTool.migrate_routes()
    
def print_routes(route_weather_pairs):
    print("\n=== Lista rekomendowanych tras ===")
    for route, weather in route_weather_pairs:
        print(f"{route.id}. {route.name}  ({route.region})")
        print(f"    Długość: {route.length_km} km")
        print(f"    Trudność: {route.difficulty}/5")
        print(f"    Szacowany czas: {route.estimated_completion()} h")
        print(f"    Komfort pogodowy: {weather.comfort_index()}")
        print(f"    Tagi: {', '.join(route.tags)}\n")

    