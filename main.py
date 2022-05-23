from PyQt5 import QtWidgets
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMessageBox
import dialog
from form import Ui_MainWindow
from dialog import Ui_Dialog

from funcs import Funcs
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

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

        self.addRowButton.clicked.connect(
            lambda: self.add_row())
        self.delRowButton.clicked.connect(
            lambda: self.del_row())


        #self.tableView.dataChanged((0, 0), (self.model.rowCount() - 1, self.model.columnCount() - 1)).connect(self.model.submitAll())

    def open_table(self, bd_name, table_name):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(bd_name)
        db.open()
        self.model = QSqlTableModel(self)
        self.model.setTable(table_name)
        self.model.select()
        self.tableView.setModel(self.model)


    def set_result(self, result):
        self.dialog = Dialog()
        self.dialog.show()
        self.dialog.labelResult.setText(result)

        self.dialog.okButton.clicked.connect(lambda: self.dialog.close())

    def add_row(self):
        try:
            self.model.insertRow(self.model.rowCount())
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Таблица не выбрана")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def del_row(self):
        try:
            selected = self.tableView.selectedIndexes()

            rows = set(index.row() for index in selected)
            rows = list(rows)
            rows.sort()
            first = rows[0]

            self.model.removeRow(first)
            self.model.select()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Выделите строку для удаления")
            msg.setWindowTitle("Ошибка")
            msg.exec_()






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
