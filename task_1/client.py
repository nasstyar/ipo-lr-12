class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя должно быть непустой строкой.")
        if not isinstance(cargo_weight, (int, float)) or cargo_weight <= 0:
            raise ValueError("Вес груза должен быть положительным числом.")
        if not isinstance(is_vip, bool):
            raise ValueError("VIP-статус должен быть True или False.")
        
        self.name = name.strip()
        self.cargo_weight = float(cargo_weight)
        self.is_vip = is_vip