from src.data_handlers.route_data_manager import RouteDataManager


def main():

    trails = RouteDataManager.load_trails("data/routes/routes.csv")

    for r in trails[:3]:
        print(r.name, "midpoint:", r.midpoint)

main()