# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from crearApp import *
from removePage import *
from buscador import *
import sys

class Ui_Main(object):
    def __init__(self,id, password):
        self.id=id
        self.password = password

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(422, 450)
        Form.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.logo = QtWidgets.QLabel(Form)
        self.logo.setGeometry(QtCore.QRect(35, 20, 350, 191))
        self.logo.setPixmap(QtGui.QPixmap("Logo.png"))
        self.logo.setText("")
        self.logo.setObjectName("logo")
        self.consultarButton = QtWidgets.QPushButton(Form)
        self.consultarButton.setGeometry(QtCore.QRect(70, 250, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.consultarButton.setFont(font)
        self.consultarButton.setStyleSheet("background-color: rgb(255, 189, 74);")
        self.consultarButton.setObjectName("consultarButton")
        self.deleteButton = QtWidgets.QPushButton(Form)
        self.deleteButton.setGeometry(QtCore.QRect(70, 350, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.deleteButton.setFont(font)
        self.deleteButton.setStyleSheet("background-color: rgb(172, 172, 172);\n"
"")
        self.deleteButton.setObjectName("deleteButton")
        self.addButton = QtWidgets.QPushButton(Form)
        self.addButton.setGeometry(QtCore.QRect(230, 250, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addButton.setFont(font)
        self.addButton.setStyleSheet("background-color: rgb(172, 172, 172);\n"
"")
        self.addButton.setObjectName("addButton")
        self.exitButton = QtWidgets.QPushButton(Form)
        self.exitButton.setGeometry(QtCore.QRect(230, 350, 121, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("background-color: rgb(255, 189, 74);")
        self.exitButton.setObjectName("exitButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def goConsulta(self, Form):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_Buscador(self.id, self.password)
        self.ui.setupUi(self.window)
        self.window.show()

    def goAdd(self, Form):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_NewApp(self.id, self.password)
        self.ui.setupUi(self.window)
        self.window.show()

    def goDelete(self, Form):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_Eliminar(self.id, self.password)
        self.ui.setupUi(self.window)
        self.window.show()

    def goExit(self, Form):
        sys.exit()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Main"))
        self.consultarButton.setText(_translate("Form", "Consultar"))
        self.deleteButton.setText(_translate("Form", "Eliminar"))
        self.addButton.setText(_translate("Form", "Agregar"))
        self.exitButton.setText(_translate("Form", "Salir"))
        self.consultarButton.clicked.connect(lambda:self.goConsulta(Form))
        self.deleteButton.clicked.connect(lambda:self.goDelete(Form))
        self.addButton.clicked.connect(lambda:self.goAdd(Form))
        self.exitButton.clicked.connect(lambda:self.goExit(Form))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Main()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
