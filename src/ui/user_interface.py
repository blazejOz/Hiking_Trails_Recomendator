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
            pass
            #find_recommended_routes()
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



        
   
def print_routes(route_weather_pairs):
    print("\n=== Lista rekomendowanych tras ===")
    for route, weather in route_weather_pairs:
        print(f"{route.id}. {route.name}  ({route.region})")
        print(f"    Długość: {route.length_km} km")
        print(f"    Trudność: {route.difficulty}/3")
        print(f"    Szacowany czas: {route.estimated_completion()} h")
        print(f"    Komfort pogodowy: {weather.comfort_index()}")
        print(f"    Tagi: {', '.join(route.tags)}\n")

    