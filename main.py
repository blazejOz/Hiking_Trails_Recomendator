from src.database.database_manager import DatabaseManager
from src.ui.user_interface import main_menu

def run_app():
    DatabaseManager.initialize_database()
    print("Database initialized successfully.")
    main_menu()

if __name__ == '__main__':
    run_app()