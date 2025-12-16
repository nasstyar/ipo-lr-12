from transport.client import Client
from transport.truck import Truck
from transport.train import Train
from transport.transport_company import TransportCompany

def input_str(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: значение не может быть пустым.")

def input_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Ошибка: значение должно быть больше нуля.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите число.")

def input_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Ошибка: значение должно быть целым и больше нуля.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")

def input_bool(prompt):
    while True:
        ans = input(prompt + " (да/нет): ").strip().lower()
        if ans in ('да', 'yes', 'y', '1'):
            return True
        elif ans in ('нет', 'no', 'n', '0'):
            return False
        print("Введите 'да' или 'нет'.")

def main():
    print("Система управления транспортной компанией")
    company_name = input_str("Введите название компании: ")
    company = TransportCompany(company_name)

    while True:
        print("\n--- Меню ---")
        print("1. Добавить клиента")
        print("2. Добавить грузовик")
        print("3. Добавить поезд")
        print("4. Показать транспорт")
        print("5. Распределить грузы")
        print("6. Выход")
        choice = input("Ваш выбор: ").strip()

        try:
            if choice == '1':
                name = input_str("Имя клиента: ")
                weight = input_float("Вес груза (в тоннах): ")
                vip = input_bool("VIP-клиент?")
                client = Client(name, weight, vip)
                company.add_client(client)
                print(f"Клиент '{name}' добавлен.")

            elif choice == '2':
                cap = input_float("Грузоподъемность (т): ")
                color = input_str("Цвет грузовика: ")
                truck = Truck(cap, color)
                company.add_vehicle(truck)
                print(f"Грузовик (ID: {truck.vehicle_id}) добавлен.")

            elif choice == '3':
                cap = input_float("Грузоподъемность (т): ")
                cars = input_int("Количество вагонов: ")
                train = Train(cap, cars)
                company.add_vehicle(train)
                print(f"Поезд (ID: {train.vehicle_id}) добавлен.")

            elif choice == '4':
                vehicles = company.list_vehicles()
                if not vehicles:
                    print("Нет транспорта.")
                else:
                    for v in vehicles:
                        print("  -", v)

            elif choice == '5':
                if not company.clients:
                    print("Нет клиентов.")
                elif not company.vehicles:
                    print("Нет транспорта.")
                else:
                    remaining = company.optimize_cargo_distribution()
                    print("\nРезультат распределения:")
                    for v in company.vehicles:
                        print(f"\n{v}")
                        if v.clients_list:
                            for c in v.clients_list:
                                print(f"  → {c.name} ({c.cargo_weight} т, VIP: {c.is_vip})")
                        else:
                            print("  (пусто)")
                    if remaining:
                        print("\nНе удалось загрузить:")
                        for c in remaining:
                            print(f"  → {c.name} ({c.cargo_weight} т)")

            elif choice == '6':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Введите число от 1 до 6.")

        except Exception as e:
            print(f" Ошибка: {e}")

if __name__ == "__main__":
    main()