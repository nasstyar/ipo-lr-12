import random
import string

class Vehicle:
    def __init__(self, capacity):
        if not isinstance(capacity, (int, float)) or capacity <= 0:
            raise ValueError("Грузоподъемность должна быть положительным числом.")
        self.vehicle_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.capacity = float(capacity)
        self.current_load = 0.0
        self.clients_list = []

    def load_cargo(self, client):
        if not hasattr(client, 'name') or not hasattr(client, 'cargo_weight'):
            raise TypeError("Объект должен быть клиентом с атрибутами 'name' и 'cargo_weight'.")
        if not isinstance(client.cargo_weight, (int, float)) or client.cargo_weight <= 0:
            raise ValueError("Вес груза клиента некорректен.")
        
        if self.current_load + client.cargo_weight > self.capacity:
            raise ValueError("Недостаточно места в транспорте для этого груза.")
        
        self.current_load += client.cargo_weight
        self.clients_list.append(client)

    def __str__(self):
        return f"Транспорт ID: {self.vehicle_id}, грузоподъемность: {self.capacity} т, загрузка: {self.current_load:.2f} т"