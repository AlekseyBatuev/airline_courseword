# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.labelResult = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelResult.setFont(font)
        self.labelResult.setText("")
        self.labelResult.setAlignment(QtCore.Qt.AlignCenter)
        self.labelResult.setObjectName("labelResult")
        self.gridLayout.addWidget(self.labelResult, 1, 0, 1, 1)
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setObjectName("okButton")
        self.gridLayout.addWidget(self.okButton, 2, 0, 1, 1)
        self.tableViewDialog = QtWidgets.QTableView(Dialog)
        self.tableViewDialog.setObjectName("tableViewDialog")
        self.gridLayout.addWidget(self.tableViewDialog, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Результат"))
        self.okButton.setText(_translate("Dialog", "Ок"))
