# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logIn.ui'
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

from keychain import init
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox
#from Actions import Ui_bienvenidaLabel
#from SignIn import Ui_LogIn
from SignIn import *
import psycopg2
from config import config
from main import *

from trusted import *


class Ui_SignInWidget(object):
    #print("estoy aqui primer")
    def setupUi(self, SignInWidget):
        #print("estoy aqui segundo")
        self.SignInWidget=SignInWidget
        SignInWidget.setObjectName("SignInWidget")
        SignInWidget.resize(322, 341)
        SignInWidget.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(236, 236, 236);")
        SignInWidget.setWindowIcon(QIcon('icono.png'))
        self.userLabel = QtWidgets.QLabel(SignInWidget)
        self.userLabel.setGeometry(QtCore.QRect(30, 60, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.userLabel.setFont(font)
        self.userLabel.setObjectName("userLabel")
        self.passwordLabel = QtWidgets.QLabel(SignInWidget)
        self.passwordLabel.setGeometry(QtCore.QRect(30, 110, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setObjectName("passwordLabel")
        self.userInput = QtWidgets.QLineEdit(SignInWidget)
        self.userInput.setGeometry(QtCore.QRect(130, 60, 151, 21))
        self.userInput.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"color: rgb(72, 72, 72);")
        self.userInput.setObjectName("userInput")
        self.passwordInput = QtWidgets.QLineEdit(SignInWidget)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setGeometry(QtCore.QRect(130, 110, 151, 20))
        self.passwordInput.setStyleSheet("background-color: rgb(243, 243, 243);\n"
"color: rgb(72, 72, 72);")
        self.passwordInput.setObjectName("passwordInput")
        self.signIn = QtWidgets.QPushButton(SignInWidget)
        self.signIn.setGeometry(QtCore.QRect(90, 250, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.signIn.setFont(font)
        self.signIn.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);")
        self.signIn.setObjectName("signIn")
        #
        self.logIn = QtWidgets.QPushButton(SignInWidget)
        self.logIn.setGeometry(QtCore.QRect(90, 180, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.logIn.setFont(font)
        self.logIn.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);")
        self.logIn.setObjectName("logIn")
        #aqui en vez de openActions seria validate para validar la data ingresada
        self.logIn.clicked.connect(self.init)
        self.retranslateUi(SignInWidget)
        #self.openActions(SignInWidget)
        QtCore.QMetaObject.connectSlotsByName(SignInWidget)

    def retranslateUi(self, SignInWidget):
        _translate = QtCore.QCoreApplication.translate
        SignInWidget.setWindowTitle(_translate("SignInWidget", "Log In"))
        self.userLabel.setText(_translate("SignInWidget", "Correo:"))
        self.passwordLabel.setText(_translate("SignInWidget", "Contraseña:"))
        self.signIn.setText(_translate("SignInWidget", "Sign In"))
        self.logIn.setText(_translate("SignInWidget", "Log In"))
        self.signIn.clicked.connect(lambda:self.openSignIn(SignInWidget))
        self.logIn.clicked.connect(lambda:self.openActions(SignInWidget))

    def openActions(self, SignInWidget):
        #Aqui iria verificar el user y password en BD
        conexion=None
        try:
            params = configmain()

            params2=config()

            #print(params)
            # Conexion al servidor de PostgreSQL
            #print('Conectando a la base de datos PostgreSQL...')
            conexion = psycopg2.connect(**params)

            conexion2 = psycopg2.connect(**params2)

            # creación del cursor
            cur = conexion.cursor()

            cur2 = conexion2.cursor()

            # Ejecución la consulta para obtener la conexión
            print('La version de PostgreSQL es la:')
            cur.execute('SELECT version()')

            # Se obtienen los resultados
            db_version = cur.fetchone()
            user=self.userInput.text()
            password=self.passwordInput.text()
            print("hizo click")

            if user != '' and password != '':
                """cur.execute("SELECT contraseña FROM permisos_usuario JOIN customer ON customer.customerid=permisos_usuario.customerid  WHERE customer.email=%s",(user,))
                contrasenaUsuario=cur.fetchall()
                print(password)
                cur.execute("SELECT permisos_usuario.permisoid FROM permisos_usuario JOIN customer ON customer.customerid=permisos_usuario.customerid  WHERE customer.email=%s",(user,))
                idUsuario=cur.fetchall()"""
                confirmation=init(user, password)
                """if (len(contrasenaUsuario)==0):
                    invalid=QMessageBox()
                    invalid.setIcon(QMessageBox.Information)
                    invalid.setWindowTitle("INVALIDO")
                    invalid.setText("Correo no registrado")
                    invalid.exec()"""
                
                if confirmation:

                    print ("entró")
                    cur.execute("SELECT id FROM users WHERE email=%s", (self.userInput.text(),))
                    idUsuario=cur.fetchall()
                    cur2.execute("SELECT password FROM passwords WHERE userid=%s", (idUsuario[0][0],))
                    passwordsList=cur2.fetchall()
                    print(passwordsList)
                    if (len(passwordsList)==0):
                        self.window = QtWidgets.QWidget()
                        self.id=idUsuario[0][0]
                        #print(self.id, password)
                        self.ui = Ui_Main(self.id, password)
                        self.ui.setupUi(self.window)
                        SignInWidget.hide()
                        self.window.show()
                    else:
                        self.window = QtWidgets.QWidget()
                        self.id=idUsuario[0][0]
                        #print(self.id, password)
                        self.ui = Ui_trustedData(self.id, password)
                        self.ui.setupUi(self.window)
                        SignInWidget.hide()
                        self.window.show()

                else: 
                    invalid=QMessageBox()
                    invalid.setIcon(QMessageBox.Information)
                    invalid.setWindowTitle("INVALIDO")
                    invalid.setText("Algo salió mal, datos incorrectos")
                    print("No entró")
                    invalid.exec()


            else:
                blank=QMessageBox()
                blank.setIcon(QMessageBox.Information)
                blank.setWindowTitle("INCOMPLETO")
                blank.setText("Por favor llene los campos")
                blank.exec()
        
            cur.close()
            cur2.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()
            if conexion2 is not None:
                conexion2.close()


    def openSignIn(self, SignInWidget):
        self.window = QtWidgets.QWidget()
        self.ui = Ui_LogIn()
        self.ui.setupUi(self.window)
        #SignInWidget.hide()
        self.window.show()

    def init(self): #log in
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
            cur.execute("SELECT hash_user FROM users WHERE email=%s", (self.userInput.text(),))
            encrypted=cur.fetchall()
            encrypted=encrypted[0][0]
            
            master=self.passwordInput.text()
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
            #print(cleartext)
            # Escribir el archivo con el texto encriptado
            try:
                print(cleartext.decode("utf-8") )#trustDataCheck PREGUNTAR A SURIANO
                return True
            except:

                print("USTED NO PUEDE ENTRAR CON ESE USUARIO")
                return False

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
    SignInWidget = QtWidgets.QWidget()
    ui = Ui_SignInWidget()
    ui.setupUi(SignInWidget)
    SignInWidget.show()
    SignInWidget.setWindowTitle("Log In")
    sys.exit(app.exec_())
