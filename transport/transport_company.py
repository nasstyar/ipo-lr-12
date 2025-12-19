from .client import Client
from .vehicle import Vehicle

class TransportCompany:
    def __init__(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Название компании должно быть непустой строкой.")
        self.name = name.strip()
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError("Можно добавлять только объекты класса Vehicle или его наследников.")
        self.vehicles.append(vehicle)

    def add_client(self, client):
        if not isinstance(client, Client):
            raise TypeError("Можно добавлять только объекты класса Client.")
        self.clients.append(client)

    def list_vehicles(self):
        return self.vehicles

    def optimize_cargo_distribution(self):

        for v in self.vehicles:
            v.current_load = 0.0
            v.clients_list = []

        sorted_clients = sorted(self.clients, key=lambda c: c.is_vip, reverse=True)
        remaining = []

        for client in sorted_clients:
            loaded = False
            for vehicle in self.vehicles:
                try:
                    vehicle.load_cargo(client)  
                    loaded = True
                    break
                except ValueError:
                    continue  
            if not loaded:
                remaining.append(client)

        return remaining