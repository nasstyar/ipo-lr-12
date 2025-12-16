from .vehicle import Vehicle

class Truck(Vehicle):
    def __init__(self, capacity, color):
        if not isinstance(color, str) or not color.strip():
            raise ValueError("Цвет должен быть непустой строкой.")
        super().__init__(capacity)
        self.color = color.strip()

    def __str__(self):
        return f"Грузовик ID: {self.vehicle_id}, цвет: {self.color}, грузоподъемность: {self.capacity} т, загрузка: {self.current_load:.2f} т"