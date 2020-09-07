# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trusted.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import psycopg2
from buscador import *
from config import config
from configmain import configmain
import hashlib
import math
import os
import hashlib
from Crypto.Cipher import AES

from Crypto.Hash import HMAC, SHA256

class Ui_trustedData(object):
    def __init__(self,id, password):
        self.id=id
        self.passwordUser = password

    def setupUi(self, trustedData):
        trustedData.setObjectName("trustedData")
        trustedData.resize(400, 196)
        trustedData.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.label = QtWidgets.QLabel(trustedData)
        self.label.setGeometry(QtCore.QRect(110, 10, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 189, 74);")
        self.label.setObjectName("label")
        self.tdcInput = QtWidgets.QLineEdit(trustedData)
        self.tdcInput.setGeometry(QtCore.QRect(100, 70, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tdcInput.setFont(font)
        self.tdcInput.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.tdcInput.setObjectName("tdcInput")
        self.aceptarButton = QtWidgets.QPushButton(trustedData)
        self.aceptarButton.setGeometry(QtCore.QRect(160, 140, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.aceptarButton.setFont(font)
        self.aceptarButton.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);")
        self.aceptarButton.setObjectName("aceptarButton")

        self.retranslateUi(trustedData)
        QtCore.QMetaObject.connectSlotsByName(trustedData)

    def retranslateUi(self, trustedData):
        _translate = QtCore.QCoreApplication.translate
        trustedData.setWindowTitle(_translate("trustedData", "Form"))
        self.label.setText(_translate("trustedData", "TRUSTED DATA CHECK"))
        self.aceptarButton.setText(_translate("trustedData", "Ingresar"))
        self.aceptarButton.clicked.connect(lambda:self.pressButton(trustedData))

    def getAll(self, userid):
        dic={}
        conexion = None
        try:
            # Lectura de los parámetros de conexion
            params = config()

            #print(params)
            # Conexion al servidor de PostgreSQL
            print('Conectando a la base de datos PostgreSQL...')
            conexion = psycopg2.connect(**params)
            # creación del cursor
            cur = conexion.cursor()
            # Ejecución la consulta para obtener la conexión
            print('La version de PostgreSQL es la:')
            cur.execute('SELECT version()')


            # Se obtienen los resultados
            db_version = cur.fetchone()
            # Se muestra la versión por pantalla
            print(db_version)
            cur.execute("SELECT * FROM passwords WHERE userid=%s", (userid,))
            for a,b,c,d in cur.fetchall() :
                dic[c]=d.tobytes()
            print("--------------------------------------------------")       

            cur.close()
            return (dic)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()
                print('Conexión finalizada.')

    def load(self, Upassword, representation, trustedDataCheck=None):#comparar con el hash de la sesion anterior paraa verificar integridad
        password=str.encode(Upassword)
        dicc=str.encode(str(representation))
        h = HMAC.new(password, digestmod=SHA256)
        h.update(dicc)
        print(str(h.hexdigest()))
        print(str(trustedDataCheck))
        if (str(h.hexdigest())==str(trustedDataCheck)):
            return True
        else:
            return False

    def pressButton(self, trustedData):
        resultado = self.load(self.passwordUser, self.getAll(self.id), self.tdcInput.text())
        if resultado == True:
            #puede consultar
            self.window = QtWidgets.QWidget()
            self.ui = Ui_Buscador(self.id, self.passwordUser)
            self.ui.setupUi(self.window)
            trustedData.hide()
            self.window.show()
        else:
            #esta hackeado
            invalid=QMessageBox()
            invalid.setIcon(QMessageBox.Information)
            invalid.setWindowTitle("Hacked")
            invalid.setText("Su informacion ha sido modificada")
            print("No entró")
            invalid.exec()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    trustedData = QtWidgets.QWidget()
    ui = Ui_trustedData()
    ui.setupUi(trustedData)
    trustedData.show()
    sys.exit(app.exec_())
