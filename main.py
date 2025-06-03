from src.database.database_manager import DatabaseManager

def run_app():
    DatabaseManager.initialize_database()
    print("Database initialized successfully.")

if __name__ == '__main__':
    run_app()