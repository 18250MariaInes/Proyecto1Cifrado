# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewApp.ui'
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


class Ui_NewApp(object):
    def __init__(self,id, password):
        self.id = id
        self.passwordUser = password

    def setupUi(self, NewApp):
        NewApp.setObjectName("NewApp")
        NewApp.resize(400, 340)
        NewApp.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.aplicacion = QtWidgets.QLabel(NewApp)
        self.aplicacion.setGeometry(QtCore.QRect(60, 100, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.aplicacion.setFont(font)
        self.aplicacion.setStyleSheet("color: rgb(255, 255, 255);")
        self.aplicacion.setObjectName("aplicacion")
        self.aplicacionInput = QtWidgets.QLineEdit(NewApp)
        self.aplicacionInput.setGeometry(QtCore.QRect(170, 100, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.aplicacionInput.setFont(font)
        self.aplicacionInput.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.aplicacionInput.setObjectName("aplicacionInput")
        self.addButton = QtWidgets.QPushButton(NewApp)
        self.addButton.setGeometry(QtCore.QRect(150, 230, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addButton.setFont(font)
        self.addButton.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);\n"
"")
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.set)

        self.label_2 = QtWidgets.QLabel(NewApp)
        self.label_2.setGeometry(QtCore.QRect(160, 20, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 189, 74);")
        self.label_2.setObjectName("label_2")
        self.password = QtWidgets.QLabel(NewApp)
        self.password.setGeometry(QtCore.QRect(60, 160, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.password.setFont(font)
        self.password.setStyleSheet("color: rgb(255, 255, 255);")
        self.password.setObjectName("password")
        self.passwordInput = QtWidgets.QLineEdit(NewApp)
        self.passwordInput.setGeometry(QtCore.QRect(170, 160, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.passwordInput.setFont(font)
        self.passwordInput.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.passwordInput.setObjectName("passwordInput")

        self.retranslateUi(NewApp)
        QtCore.QMetaObject.connectSlotsByName(NewApp)

    def set(self):
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
            master=self.passwordUser
            password= str.encode(master)
            #print(password)
            #se genera una cadena de bytes aleatorios (del tamano del salsize)
            
            salt = os.urandom(SALT_SIZE)
            derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                                      dklen=IV_SIZE + KEY_SIZE)
            
            #vector inicial con tamano 16
            iv = derived[0:IV_SIZE]
            #llave con tamano 32
            key = derived[IV_SIZE:]
            
            print(self.passwordInput.text())
            value=str.encode(self.passwordInput.text())

            #aqui se encripta el texto
            encrypted, authTag =  AES.new(key, AES.MODE_GCM, iv).encrypt_and_digest(value)
            # Escribir el archivo con el texto encriptado
            
            

            encrypted=salt+encrypted
            encrypted=encrypted 
            print(encrypted)

            cur.execute( """SELECT site from passwords where userid=%s and site=%s""",(self.id,self.aplicacionInput.text()))
            siteName=cur.fetchall()
            if (len(siteName)==0):
                cur.execute("INSERT INTO passwords (userid, site, password)VALUES (%s,%s, %s)", (self.id, self.aplicacionInput.text(), encrypted))
            else: 
                cur.execute("UPDATE passwords set password=%s where site=%s and userid=%s", ( encrypted, self.aplicacionInput.text(), self.id))
            

            conexion.commit()
            blank=QMessageBox()
            blank.setIcon(QMessageBox.Information)
            blank.setWindowTitle("Accion Exitosa")
            blank.setText("Se ha agregado exitosamente")
            blank.exec()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()
                print('Conexión finalizada.')



    def retranslateUi(self, NewApp):
        _translate = QtCore.QCoreApplication.translate
        NewApp.setWindowTitle(_translate("NewApp", "Nueva App"))
        self.aplicacion.setText(_translate("NewApp", "Aplicación:"))
        self.addButton.setText(_translate("NewApp", "Agregar"))
        self.label_2.setText(_translate("NewApp", "N U E V O"))
        self.password.setText(_translate("NewApp", "Contraseña:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    NewApp = QtWidgets.QWidget()
    ui = Ui_NewApp()
    ui.setupUi(NewApp)
    NewApp.show()
    sys.exit(app.exec_())
