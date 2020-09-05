# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SignIn.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

import psycopg2
from config import config
from configmain import configmain
import hashlib
import math
import os
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
#from logIn import *

from Crypto.Hash import HMAC, SHA256
from Crypto.Cipher import AES

IV_SIZE = 16    # Largo de la cadena de 128 bits, estandarizada para el algoritmo AES
KEY_SIZE = 32   # Largo de la llave de 256 bit modificado para el algoritmo AES-256 (32*8=256)
SALT_SIZE = 16  # Tamano recomendado para esta encripccion

class Ui_LogIn(object):
    def setupUi(self, LogIn):
        self.LogIn=LogIn
        LogIn.setObjectName("LogIn")
        LogIn.resize(261, 268)
        LogIn.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(236, 236, 236);")
        LogIn.setWindowIcon(QIcon('icono.png'))
        self.usernameLabel = QtWidgets.QLabel(LogIn)
        self.usernameLabel.setGeometry(QtCore.QRect(20, 40, 60, 13))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.usernameLabel.setFont(font)
        self.usernameLabel.setObjectName("usernameLabel")
        self.emailLabel = QtWidgets.QLabel(LogIn)
        self.emailLabel.setGeometry(QtCore.QRect(20, 95, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.emailLabel.setFont(font)
        self.emailLabel.setObjectName("emailLabel")
        self.passwordLabel = QtWidgets.QLabel(LogIn)
        self.passwordLabel.setGeometry(QtCore.QRect(20, 150, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.usernameInput = QtWidgets.QLineEdit(LogIn)
        self.usernameInput.setGeometry(QtCore.QRect(110, 40, 113, 20))
        self.usernameInput.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"color: rgb(72, 72, 72);")
        self.usernameInput.setObjectName("usernameInput")
        self.emailInput = QtWidgets.QLineEdit(LogIn)
        self.emailInput.setGeometry(QtCore.QRect(110, 95, 113, 20))
        self.emailInput.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"color: rgb(72, 72, 72);")
        self.emailInput.setObjectName("emailInput")
        self.passwordInput = QtWidgets.QLineEdit(LogIn)
        self.passwordInput.setGeometry(QtCore.QRect(110, 150, 113, 20))
        self.passwordInput.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"color: rgb(72, 72, 72);")
        self.passwordInput.setObjectName("passwordInput")
        self.sigInButton = QtWidgets.QPushButton(LogIn)
        self.sigInButton.setGeometry(QtCore.QRect(70, 200, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.sigInButton.setFont(font)
        self.sigInButton.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);")
        self.sigInButton.setObjectName("sigInButton")
        self.sigInButton.clicked.connect(self.sign_in_func)
        self.retranslateUi(LogIn)
        #self.validateInfo(LogIn)
        QtCore.QMetaObject.connectSlotsByName(LogIn)

    def retranslateUi(self, LogIn):
        _translate = QtCore.QCoreApplication.translate
        LogIn.setWindowTitle(_translate("LogIn", "Sign In"))
        self.usernameLabel.setText(_translate("LogIn", "Username:"))
        self.emailLabel.setText(_translate("LogIn", "Email:"))
        self.passwordLabel.setText(_translate("LogIn", "Contraseña:"))
        self.sigInButton.setText(_translate("LogIn", "Sign In"))
        self.sigInButton.clicked.connect(lambda:self.validateInfo(LogIn))

    def sign_in_func(self):
        conexion = None
        try:
            # Lectura de los parámetros de conexion
            params = configmain()

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
            master=self.passwordInput
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
            

            hash_user=str.encode(self.usernameInput)

            #aqui se encripta el texto
            encrypted, authTag =  AES.new(key, AES.MODE_GCM, iv).encrypt_and_digest(hash_user)
            # Escribir el archivo con el texto encriptado
            
            #print(authTag)#trustDataCheck PREGUNTAR A SURIANO

            encrypted=salt+encrypted ##sha de diccionario de todos los datos
            encrypted=encrypted 

            cur.execute("INSERT INTO users (username, email, hash_user)VALUES (%s,%s, %s)", (self.usernameInput, self.emailInput, encrypted))
            conexion.commit()
            cur.close()
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()
                print('Conexión finalizada.')

    def validateInfo(self, LogIn):
        #Aqui iria verificar el user y password en BD
        conexion=None
        try:
            params = config()

            #print(params)
            # Conexion al servidor de PostgreSQL
            #print('Conectando a la base de datos PostgreSQL...')
            conexion = psycopg2.connect(**params)

            # creación del cursor
            cur = conexion.cursor()

            # Ejecución la consulta para obtener la conexión
            print('La version de PostgreSQL es la:')
            cur.execute('SELECT version()')

            # Se obtienen los resultados
            db_version = cur.fetchone()
            username=self.usernameInput.text()
            email=self.emailInput.text()
            contrasena=self.passwordInput.text()
            """user=self.userInput.text()
            password=self.passwordInput.text()"""

            if (username != '' and email != '' and contrasena != '') :
                cur.execute( "SELECT firstname FROM customer WHERE customer.email=%s",(email,) )
                correo_existente=cur.fetchall()
                if (len(correo_existente)!=0):
                    blank=QMessageBox()
                    blank.setIcon(QMessageBox.Information)
                    blank.setWindowTitle("ERROR")
                    blank.setText("Ese correo ya esta registrado")
                    blank.exec()
                else:
                    cur.execute( "SELECT MAX(customer.customerid) FROM customer" )
                    IDUsuario=cur.fetchall()
                    IDoficial=(IDUsuario[0][0])
                    IDoficial += 1
                    print(IDoficial)
                    cur.execute("INSERT INTO customer (customerid, firstname, lastname, email)VALUES (%s, %s,%s, %s)", (IDoficial, username, apellido, email,))
                    cur.execute("INSERT INTO permisos_usuario (permisoid, contraseña, customerid, puede_registrar, puede_inactivar, puede_eliminar,puede_modificar)VALUES (%s, %s,%s, %s,%s,%s, %s)", (IDoficial, contrasena, IDoficial,False, False,False,False,))
                    conexion.commit()
                    """self.window = QtWidgets.QWidget()
                    self.ui = Ui_SignInWidget()
                    self.ui.setupUi(self.window)
                    #LogIn.hide()
                    self.window.show()"""
                    #LogIn.hide()
                    """self.window = QtWidgets.QWidget()
                    self.ui = Ui_SignInWidget()
                    self.ui.setupUi(self.window)"""
                    LogIn.hide()
                    #self.window.show()
            else:
                blank=QMessageBox()
                blank.setIcon(QMessageBox.Information)
                blank.setWindowTitle("INCOMPLETO")
                blank.setText("Por favor llene los campos")
                blank.exec()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LogIn = QtWidgets.QWidget()
    ui = Ui_LogIn()
    ui.setupUi(LogIn)
    LogIn.show()
    LogIn.setWindowTitle("Sign In")
    sys.exit(app.exec_())
