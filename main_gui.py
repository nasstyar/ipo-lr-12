import dearpygui.dearpygui as dpg
import json
import traceback
from transport.client import Client
from transport.truck import Truck
from transport.train import Train
from transport.transport_company import TransportCompany

dpg.create_context()

try:
    with dpg.font_registry():
        font_path = "C:/Windows/Fonts/arial.ttf"
        with dpg.font(font_path, 16) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.bind_font(font)
except Exception as e:
    print(f"Не удалось загрузить шрифт: {e}")

company = TransportCompany("Транспортная компания")

def msg(text, error=False):
    dpg.set_value("status", text)
    dpg.configure_item("status", color=(255, 0, 0) if error else (0, 255, 0))

def validate_client(name, weight):
    if not name or len(name.strip()) < 2 or not name.replace(" ", "").isalpha():
        raise ValueError("Имя: мин. 2 буквы, только буквы.")
    w = float(weight)
    if w <= 0 or w > 10000:
        raise ValueError("Вес: 0 < x ≤ 10000.")
    return name.strip(), w

def validate_vehicle(cap, color=None, cars=None, vtype=None):
    cap = float(cap)
    if cap <= 0:
        raise ValueError("Грузоподъёмность > 0")
    if vtype == "Грузовик":
        if not color or not color.strip():
            raise ValueError("Цвет не может быть пустым")
        return Truck(cap, color.strip())
    else:
        cars = int(cars)
        if cars <= 0:
            raise ValueError("Вагоны > 0")
        return Train(cap, cars)

def reload_clients():
    children = dpg.get_item_children("clients_table", 1)
    for child in children:
        if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
            dpg.delete_item(child)

    for i, c in enumerate(company.clients):
        with dpg.table_row(parent="clients_table", tag=f"client_row_{i}"):
            dpg.add_checkbox(tag=f"cb_client_{i}")
            dpg.add_text(c.name)
            dpg.add_text(f"{c.cargo_weight:.2f}")
            dpg.add_text("Да" if c.is_vip else "Нет")

def reload_vehicles():
    children = dpg.get_item_children("vehicles_table", 1)
    for child in children:
        if dpg.get_item_type(child) == "mvAppItemType::mvTableRow":
            dpg.delete_item(child)

    for i, v in enumerate(company.vehicles):
        t = "Грузовик" if isinstance(v, Truck) else "Поезд"
        with dpg.table_row(parent="vehicles_table", tag=f"vehicle_row_{i}"):
            dpg.add_checkbox(tag=f"cb_vehicle_{i}")
            dpg.add_text(v.vehicle_id)
            dpg.add_text(t)
            dpg.add_text(f"{v.capacity:.2f}")
            dpg.add_text(f"{v.current_load:.2f}")

def add_client():
    try:
        name, w = validate_client(dpg.get_value("n"), dpg.get_value("w"))
        vip = dpg.get_value("v")
        client = Client(name, w, vip)
        company.add_client(client)
        reload_clients()
        msg("Клиент добавлен")
        dpg.delete_item("win_client")
    except Exception as e:
        msg(str(e), error=True)

def add_vehicle():
    try:
        vt = dpg.get_value("vt")
        cap = dpg.get_value("c")
        if vt == "Грузовик":
            col = dpg.get_value("col")
            v = validate_vehicle(cap, color=col, vtype=vt)
        else:
            cars = dpg.get_value("cars")
            v = validate_vehicle(cap, cars=cars, vtype=vt)
        company.add_vehicle(v)
        reload_vehicles()
        msg(f"{vt} добавлен")
        dpg.delete_item("win_vehicle")
    except Exception as e:
        msg(str(e), error=True)

def open_add_client():
    if dpg.does_item_exist("win_client"):
        dpg.delete_item("win_client")
    with dpg.window(label="Новый клиент", tag="win_client", width=300, pos=[100,100]):
        dpg.add_input_text(tag="n", label="Имя")
        dpg.add_input_float(tag="w", default_value=1.0, label="Вес (т)")
        dpg.add_checkbox(tag="v", label="VIP")
        dpg.add_button(label="Сохранить", callback=add_client)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("win_client"))

def open_add_vehicle():
    if dpg.does_item_exist("win_vehicle"):
        dpg.delete_item("win_vehicle")
    def toggle(_, data):
        dpg.configure_item("col", show=(data == "Грузовик"))
        dpg.configure_item("cars", show=(data == "Поезд"))
    with dpg.window(label="Новый транспорт", tag="win_vehicle", width=300, pos=[100,100]):
        dpg.add_combo(["Грузовик", "Поезд"], default_value="Грузовик", callback=toggle, tag="vt")
        dpg.add_input_float(tag="c", default_value=10.0, label="Грузоподъёмность (т)")
        dpg.add_input_text(tag="col", label="Цвет", show=True)
        dpg.add_input_int(tag="cars", default_value=1, label="Вагоны", show=False)
        dpg.add_button(label="Сохранить", callback=add_vehicle)
        dpg.add_button(label="Отмена", callback=lambda: dpg.delete_item("win_vehicle"))

def delete_clients():
    to_del = []
    for i in range(len(company.clients)):
        try:
            if dpg.get_value(f"cb_client_{i}"):
                to_del.append(i)
        except:
            continue

    if not to_del:
        return msg("Выберите клиентов", error=True)

    for i in sorted(to_del, reverse=True):
        del company.clients[i]

    reload_clients()
    msg(f"Удалено: {len(to_del)} клиентов")

def delete_vehicles():
    to_del = []
    for i in range(len(company.vehicles)):
        try:
            if dpg.get_value(f"cb_vehicle_{i}"):
                to_del.append(i)
        except:
            continue

    if not to_del:
        return msg("Выберите транспорт", error=True)

    for i in sorted(to_del, reverse=True):
        del company.vehicles[i]

    reload_vehicles()
    msg(f"Удалено: {len(to_del)} единиц")

def run_optimize():
    try:
        if not company.clients or not company.vehicles:
            return msg("Нет клиентов или транспорта", error=True)

        for v in company.vehicles:
            v.current_load = 0.0
            v.clients_list = []

        remaining = company.optimize_cargo_distribution()

        reload_vehicles()

        dpg.delete_item("distribution_result_window", children_only=True)

        for v in company.vehicles:
            dpg.add_text(str(v), parent="distribution_result_window")
            for c in v.clients_list:
                dpg.add_text(f" - {c.name} ({c.cargo_weight:.2f} т, VIP: {c.is_vip})", parent="distribution_result_window")
        
        if remaining:
            dpg.add_separator(parent="distribution_result_window")
            dpg.add_text("Не загружены:", parent="distribution_result_window")
            for c in remaining:
                dpg.add_text(f" - {c.name} ({c.cargo_weight:.2f} т, VIP: {'Да' if c.is_vip else 'Нет'})", parent="distribution_result_window")
        
        dpg.add_button(label="Закрыть", callback=lambda: dpg.hide_item("distribution_result_window"), parent="distribution_result_window")

        dpg.show_item("distribution_result_window")

    except Exception as e:
        print("Ошибка в run_optimize:")
        traceback.print_exc()
        msg(f"Ошибка: {e}", error=True)

def export_result():
    if not company.clients or not company.vehicles:
        return msg("Нет данных для экспорта", error=True)
    data = {
        "clients": [{"name": c.name, "weight": c.cargo_weight, "vip": c.is_vip} for c in company.clients],
        "vehicles": []
    }
    for v in company.vehicles:
        base = {
            "id": v.vehicle_id,
            "type": "truck" if isinstance(v, Truck) else "train",
            "capacity": v.capacity,
            "load": v.current_load,
            "clients": [{"name": c.name, "weight": c.cargo_weight, "vip": c.is_vip} for c in v.clients_list]
        }
        if isinstance(v, Truck):
            base["color"] = v.color
        else:
            base["cars"] = v.number_of_cars
        data["vehicles"].append(base)
    with open("distribution_result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    msg("Результат сохранён в distribution_result.json")

def about():
    with dpg.window(label="О программе", modal=True, width=400, height=200, pos=[300,300]):
        dpg.add_text("Лабораторная работа 13")
        dpg.add_text("Вариант: 1")
        dpg.add_text("Разработчик: Козлова Анастасия")
        dpg.add_button(label="Закрыть", callback=lambda: dpg.delete_item(dpg.get_active_window()))

with dpg.window(tag="Main"):
    with dpg.menu_bar():
        dpg.add_menu_item(label="Экспорт результата", callback=export_result)
        dpg.add_menu_item(label="О программе", callback=about)

    with dpg.group(horizontal=True):
        with dpg.child_window(width=220):
            dpg.add_button(label="Добавить клиента", callback=open_add_client, width=200)
            dpg.add_button(label="Добавить транспорт", callback=open_add_vehicle, width=200)
            dpg.add_button(label="Распределить грузы", callback=run_optimize, width=200)
            dpg.add_separator()
            dpg.add_button(label="Удалить клиентов", callback=delete_clients, width=200)
            dpg.add_button(label="Удалить транспорт", callback=delete_vehicles, width=200)

        with dpg.child_window():
            dpg.add_text("Клиенты")
            with dpg.table(header_row=True, tag="clients_table"):
                dpg.add_table_column(label="Выбрать")
                dpg.add_table_column(label="Имя")
                dpg.add_table_column(label="Вес (т)")
                dpg.add_table_column(label="VIP")

            dpg.add_spacer(height=20)

            dpg.add_text("Транспорт")
            with dpg.table(header_row=True, tag="vehicles_table"):
                dpg.add_table_column(label="Выбрать")
                dpg.add_table_column(label="ID")
                dpg.add_table_column(label="Тип")
                dpg.add_table_column(label="Грузоподъёмность")
                dpg.add_table_column(label="Загрузка")

    dpg.add_text("", tag="status")

with dpg.window(
    tag="distribution_result_window",
    label="Результат распределения",
    modal=True,
    show=False,
    width=600,
    height=450,
    pos=[200, 150],
    no_resize=True,
    no_collapse=True
):
    pass

reload_clients()
reload_vehicles()

dpg.create_viewport(title='ЛР13 — Транспорт', width=1000, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()