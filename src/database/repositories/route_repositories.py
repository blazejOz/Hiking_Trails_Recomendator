class RouteRepository:
    def __init__(self, db):
        self.db = db

    def get_all_routes(self):
        return self.db.query("SELECT * FROM routes")

    def get_route_by_id(self, route_id):
        return self.db.query("SELECT * FROM routes WHERE id = ?", (route_id,))

    def create_route(self, route_data):
        return self.db.execute("INSERT INTO routes (name, description) VALUES (?, ?)", 
                               (route_data['name'], route_data['description']))

    def update_route(self, route_id, route_data):
        return self.db.execute("UPDATE routes SET name = ?, description = ? WHERE id = ?", 
                               (route_data['name'], route_data['description'], route_id))

    def delete_route(self, route_id):
        return self.db.execute("DELETE FROM routes WHERE id = ?", (route_id,))