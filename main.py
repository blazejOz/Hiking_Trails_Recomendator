from src.data_handlers.route_data_manager import RouteDataManager


def main():

    trails = RouteDataManager.load_trails("data/routes/routes.csv")

main()