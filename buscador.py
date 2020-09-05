# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Buscador.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from config import config
from configmain import configmain
import hashlib
import math
import os
import hashlib
from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
#from Actions import Ui_bienvenidaLabel
#from SignIn import Ui_LogIn
from SignIn import *
import psycopg2
from config import config

class Ui_Buscador(object):
    def setupUi(self, Buscador):
        Buscador.setObjectName("Buscador")
        Buscador.resize(400, 275)
        Buscador.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.aplicacion = QtWidgets.QLabel(Buscador)
        self.aplicacion.setGeometry(QtCore.QRect(60, 100, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.aplicacion.setFont(font)
        self.aplicacion.setStyleSheet("color: rgb(255, 255, 255);")
        self.aplicacion.setObjectName("aplicacion")
        self.aplicacionInput = QtWidgets.QLineEdit(Buscador)
        self.aplicacionInput.setGeometry(QtCore.QRect(170, 100, 181, 31))
        self.aplicacionInput.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.aplicacionInput.setObjectName("aplicacionInput")
        self.consultarButton = QtWidgets.QPushButton(Buscador)
        self.consultarButton.setGeometry(QtCore.QRect(150, 180, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.consultarButton.setFont(font)
        self.consultarButton.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);\n"
"")
        self.consultarButton.setObjectName("consultarButton")
        self.consultarButton.clicked.connect(self.get)

        self.label_2 = QtWidgets.QLabel(Buscador)
        self.label_2.setGeometry(QtCore.QRect(120, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 189, 74);")
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Buscador)
        QtCore.QMetaObject.connectSlotsByName(Buscador)

    def retranslateUi(self, Buscador):
        _translate = QtCore.QCoreApplication.translate
        Buscador.setWindowTitle(_translate("Buscador", "Buscador"))
        self.aplicacion.setText(_translate("Buscador", "Aplicación:"))
        self.consultarButton.setText(_translate("Buscador", "Consultar"))
        self.label_2.setText(_translate("Buscador", "B U S C A D O R "))

    def get(self):
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
            cur.execute("SELECT password FROM passwords WHERE userid=%s and site=%s", (2, self.aplicacionInput.text()))
            encrypted=cur.fetchall()
            encrypted=encrypted[0][0]
            
            master="camila"
            password= str.encode(master)
            

            salt = encrypted[0:SALT_SIZE]
            #print(password)
            #se genera una cadena de bytes aleatorios (del tamano del salsize)
            
            derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                                      dklen=IV_SIZE + KEY_SIZE)
            
            #vector inicial con tamano 16
            iv = derived[0:IV_SIZE]
            #llave con tamano 32
            key = derived[IV_SIZE:]
            
            

            #aqui se encripta el texto
            cleartext =  AES.new(key, AES.MODE_GCM, iv).decrypt(encrypted[SALT_SIZE:])
            # Escribir el archivo con el texto encriptado
            
            print(cleartext.decode("utf-8") )#trustDataCheck PREGUNTAR A SURIANO

            

            
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()
                print('Conexión finalizada.')



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Buscador = QtWidgets.QWidget()
    ui = Ui_Buscador()
    ui.setupUi(Buscador)
    Buscador.show()
    sys.exit(app.exec_())
