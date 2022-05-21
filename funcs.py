import sqlite3
from itertools import chain
import json

from PyQt5 import QtWidgets
from PyQt5.Qt import *

from form import Ui_MainWindow

airline_bd = sqlite3.connect('Airline.db')
airports_bd = sqlite3.connect("Airports.db")
parking_bd = sqlite3.connect("Parking.db")
airline_cur = airline_bd.cursor()
airports_cur = airports_bd.cursor()
parking_cur = parking_bd.cursor()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



        # 1. Создайте соединение с базой данных, вызвав метод addDatabase() класса QSqlDatabase.
        #    Так как вы хотите соединиться с базой данных SQLite, параметры QSQLITE передаются здесь.
        db = QSqlDatabase.addDatabase('QSQLITE')

        # 2. Вызовите setDatabaseName(), чтобы установить имя базы данных, которое будет использоваться.
        #    Вам нужно только написать путь, а имя файла заканчивается на .db
        #   (если база данных уже существует, используйте базу данных; если она не существует,
        #    будет создана новая);
        db.setDatabaseName('Airline.db')  # !!! ваша db

        # 3. Вызовите метод open(), чтобы открыть базу данных.
        #    Если открытие прошло успешно, оно вернет True, а в случае неудачи - False.
        db.open()

        # Создайте модель QSqlTableModel и вызовите setTable(),
        # чтобы выбрать таблицу данных для обработки.
        self.model = QSqlTableModel(self)
        self.model.setTable("Flights")  # !!! таблица в db

        # вызовите метод select(), чтобы выбрать все данные в таблице, и соответствующее
        # представление также отобразит все данные;
        self.model.select()
        self.tableView.setModel(self.model)

        self.rentabButton.clicked.connect(self.set_result(flights_profitability()))
        self.naletButton.clicked.connect(self.set_result(flight_time()))
        self.zapolnButton.clicked.connect(self.set_result(flight_occupancy()))
        self.prostoiButton.clicked.connect(self.set_result(parking_cost()))

    def open_table(self):
        print("еще не сделал")

    def set_result(self, result):
        self.labelResult.setText(result)
        
# 1. Посчитать рентабельность рейсов
def flights_profitability():
    print("start")

    jet_id, airports, ticket_price, number_of_tickets_sold, depreciation_cost, fuel_cost = list(zip(*airline_cur.execute(f'''
        SELECT jet_id, arrival_point, ticket_price, number_of_tickets_sold, depreciation_cost, fuel_cost 
        FROM Flights
    ''').fetchall()))

    models = [airline_bd.execute(f'''
        SELECT model_name 
        FROM "Jets" 
        WHERE jet_id == "{i}"
    ''').fetchone()[0] for i in jet_id]

    classes = [airline_bd.execute(f'''
        SELECT class_name 
        FROM "Models" 
        WHERE model_name == "{i}"
    ''').fetchone()[0] for i in models]

    maintenance_cost = [airports_cur.execute(f'''
        SELECT maintenance_cost 
        FROM "{airports[i]}" 
        WHERE class == "{classes[i]}"
    ''').fetchone()[0] for i in range(len(airports))]

    income = sum(list(map(lambda x, y: x * y, ticket_price, number_of_tickets_sold)))
    expenses = sum(depreciation_cost) + sum(fuel_cost) + sum(maintenance_cost)

    print((income - expenses) / expenses)
    return str((income - expenses) / expenses)

# 2. Посчитать налет самолетов (за месяц, например)
def flight_time():
    print("start")
    jet_id = list(chain(*airline_cur.execute(f'SELECT jet_id FROM Jets').fetchall()))
    travel_times_list = [airline_bd.execute(f'''
        SELECT travel_time 
        FROM Flights 
        WHERE jet_id == "{i}"
    ''').fetchall() for i in jet_id]

    print(dict(zip(jet_id, [sum(list(chain(*lists_of_lists))) for lists_of_lists in travel_times_list])))
    return dict(zip(jet_id, [sum(list(chain(*lists_of_lists))) for lists_of_lists in travel_times_list]))

# 3. Посчитать “заполняемость” рейса в % за месяц.
def flight_occupancy():
    print("start")
    flight_id, jet_id, number_of_tickets_sold  = list(zip(*airline_cur.execute(f'''
        SELECT flight_id, jet_id, number_of_tickets_sold 
        FROM Flights
    ''').fetchall()))

    models = [airline_bd.execute(f'''
        SELECT model_name 
        FROM "Jets" 
        WHERE jet_id == "{i}"
    ''').fetchone()[0] for i in jet_id]

    number_of_passangers = [airline_bd.execute(f'''
        SELECT number_of_passengers 
        FROM "Models" 
        WHERE model_name == "{i}"
    ''').fetchone()[0] for i in models]

    ratio = list(map(lambda x, y: round(x / y, 2), number_of_tickets_sold, number_of_passangers))

    print(dict(zip(flight_id, ratio)))
    return dict(zip(flight_id, ratio))

# 4. Посчитать стоимость простоя самолетов.
def parking_cost():
    print("start")
    jet_id = list(chain(*airline_cur.execute(f'SELECT jet_id FROM Jets').fetchall()))
    models = [airline_bd.execute(f'''
        SELECT model_name 
        FROM "Jets" 
        WHERE jet_id == "{i}"
    ''').fetchone()[0] for i in jet_id]

    classes = [airline_bd.execute(f'''
        SELECT class_name 
        FROM "Models" 
        WHERE model_name == "{i}"
    ''').fetchone()[0] for i in models]

    airports = list(chain(*parking_cur.execute(f'''
        SELECT name 
        FROM sqlite_master 
        WHERE type='table';
    ''').fetchall()))

    airports.remove('sqlite_sequence')

    parking_hours = [[parking_cur.execute(f'''
        SELECT "hours" 
        FROM "{i}" 
        WHERE jet_id == "{j}"
    ''').fetchall()[0][0] for i in airports] for j in jet_id]

    airports_hours_dict = list(dict(zip(airports, i)) for i in parking_hours)

    cost_dict = [[airports_bd.execute(f'''
        SELECT parking_cost 
        FROM "{key}" 
        WHERE class == "{classes[i]}"
    ''').fetchone()[0] * val for key, val in airports_hours_dict[i].items()] for i in range(len(classes))]

    print(sum(map(sum, cost_dict)))
    return sum(map(sum, cost_dict))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

