from .vehicle import Vehicle

class Train(Vehicle):
    def __init__(self, capacity, number_of_cars):
        if not isinstance(number_of_cars, int) or number_of_cars <= 0:
            raise ValueError("Количество вагонов должно быть целым положительным числом.")
        super().__init__(capacity)
        self.number_of_cars = number_of_cars

    def __str__(self):
        return f"Поезд ID: {self.vehicle_id}, вагонов: {self.number_of_cars}, грузоподъемность: {self.capacity} т, загрузка: {self.current_load:.2f} т"