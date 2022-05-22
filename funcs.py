import sqlite3
from itertools import chain

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

        self.rentabButton.clicked.connect(lambda: self.set_result(flights_profitability()))
        self.naletButton.clicked.connect(lambda: self.set_result(flight_time()))
        self.zapolnButton.clicked.connect(lambda: self.set_result(flight_occupancy()))
        self.prostoiButton.clicked.connect(lambda: self.set_result(parking_cost()))

        self.actionClasses.triggered.connect(
            lambda: self.open_table(self.menuAirline_db.title(), self.actionClasses.text()))
        self.actionFlights.triggered.connect(
            lambda: self.open_table(self.menuAirline_db.title(), self.actionFlights.text()))
        self.actionJets.triggered.connect(
            lambda: self.open_table(self.menuAirline_db.title(), self.actionJets.text()))
        self.actionModels.triggered.connect(
            lambda: self.open_table(self.menuAirline_db.title(), self.actionModels.text()))

        self.actionDME.triggered.connect(
            lambda: self.open_table(self.menuAirports_db.title(), self.actionDME.text()))
        self.actionLED.triggered.connect(
            lambda: self.open_table(self.menuAirports_db.title(), self.actionLED.text()))
        self.actionKZN.triggered.connect(
            lambda: self.open_table(self.menuAirports_db.title(), self.actionKZN.text()))

        self.actionDME_2.triggered.connect(
            lambda: self.open_table(self.menuParking_db.title(), self.actionDME_2.text()))
        self.actionLED_2.triggered.connect(
            lambda: self.open_table(self.menuParking_db.title(), self.actionLED_2.text()))
        self.actionKZN_2.triggered.connect(
            lambda: self.open_table(self.menuParking_db.title(), self.actionKZN_2.text()))

    def open_table(self, bd_name, table_name):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(bd_name)
        db.open()
        self.model = QSqlTableModel(self)
        self.model.setTable(table_name)
        self.model.select()
        self.tableView.setModel(self.model)
        rowPosition = self.model.rowCount()
        self.model.insertRow(rowPosition)
        self.plusRow = QtWidgets.QPushButton(self.centralwidget)

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
    return str(round(((income - expenses) / expenses), 2))

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
    return str(dict(zip(jet_id, [sum(list(chain(*lists_of_lists))) for lists_of_lists in travel_times_list])))

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
    return str(dict(zip(flight_id, ratio)))

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
    return str(sum(map(sum, cost_dict)))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

