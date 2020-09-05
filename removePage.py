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
from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem
#from Actions import Ui_bienvenidaLabel
#from SignIn import Ui_LogIn
from SignIn import *
import psycopg2
from config import config


class Ui_Eliminar(object):
    def setupUi(self, Eliminar):
        Eliminar.setObjectName("Eliminar")
        Eliminar.resize(400, 340)
        Eliminar.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.removeButton = QtWidgets.QPushButton(Eliminar)
        self.removeButton.setGeometry(QtCore.QRect(160, 260, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.removeButton.setFont(font)
        self.removeButton.setStyleSheet("background-color: rgb(206, 206, 206);\n"
"color: rgb(72, 72, 72);\n"
"")
        self.removeButton.setObjectName("removeButton")
        self.removeButton.clicked.connect(self.remove)
        self.label_2 = QtWidgets.QLabel(Eliminar)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 189, 74);")
        self.label_2.setObjectName("label_2")
        self.appsTable = QtWidgets.QTableWidget(Eliminar)
        self.appsTable.setGeometry(QtCore.QRect(140, 70, 131, 161))
        self.appsTable.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.appsTable.setObjectName("appsTable")
        self.appsTable.setColumnCount(1)
        self.appsTable.setRowCount(0)
        self.appsTable.setColumnWidth(0, 130)
        nombreColumnas = ("Aplicacion",)
        # Establecer las etiquetas de encabezado horizontal usando etiquetas
        self.appsTable.setHorizontalHeaderLabels(nombreColumnas)

        self.conectar()
        self.retranslateUi(Eliminar)
        QtCore.QMetaObject.connectSlotsByName(Eliminar)

    def retranslateUi(self, Eliminar):
        _translate = QtCore.QCoreApplication.translate
        Eliminar.setWindowTitle(_translate("Eliminar", "Form"))
        self.removeButton.setText(_translate("Eliminar", "Eliminar"))
        self.label_2.setText(_translate("Eliminar", "E L I M I N A R"))

    def conectar(self):
        #Buscar track
        self.appsTable.setRowCount(0)
        id=2
        #nombreTrack=self.inputTrack.text()
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
            print(id)
            row=0
            cur.execute( """SELECT site from passwords 
                where userid=%s""",(id,))
            for a in cur.fetchall():
                self.appsTable.setRowCount(row + 1)
                self.appsTable.setItem(row, 0, QTableWidgetItem(a[0]))
                row += 1
            cur.close()                
            
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conexion is not None:
                conexion.close()
                print('Conexión finalizada.')

    def remove(self):
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
            r = self.appsTable.currentRow()
            name=self.appsTable.item(r,0).text()
            print(name)
            cur.execute("DELETE FROM passwords WHERE passwords.userid = %s AND passwords.site=%s",(2,name))
            conexion.commit() 
            blank=QMessageBox()
            blank.setIcon(QMessageBox.Information)
            blank.setWindowTitle("Accion Exitosa")
            blank.setText("Se ha eliminado exitosamente")
            blank.exec()     
            self.conectar()
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
    Eliminar = QtWidgets.QWidget()
    ui = Ui_Eliminar()
    ui.setupUi(Eliminar)
    Eliminar.show()
    sys.exit(app.exec_())
