from PyQt5 import QtWidgets
from PyQt5.Qt import *

import dialog
from form import Ui_MainWindow
from dialog import Ui_Dialog

from funcs import Funcs


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.dialog = None
        self.plus_row = None
        self.model = None
        self.setupUi(self)

        funcs = Funcs()  # Создаю объект класса Funcs для использования его методов (функций расчета)

        self.rentabButton.clicked.connect(lambda: self.set_result(funcs.flights_profitability()))
        self.naletButton.clicked.connect(lambda: self.set_result(funcs.flight_time()))
        self.zapolnButton.clicked.connect(lambda: self.set_result(funcs.flight_occupancy()))
        self.prostoiButton.clicked.connect(lambda: self.set_result(funcs.parking_cost()))

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
        row_position = self.model.rowCount()
        self.model.insertRow(row_position)
        self.plus_row = QtWidgets.QPushButton(self.centralwidget)

    def set_result(self, result):
        self.dialog = Dialog()
        self.dialog.show()

        self.dialog.labelResult.setText(result)

        self.dialog.okButton.clicked.connect(lambda: self.dialog.close())


class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
