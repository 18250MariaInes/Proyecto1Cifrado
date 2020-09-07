# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trusted.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_trustedData(object):
    def __init__(self,id, password):
        self.id=id
        self.password = password
        
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    trustedData = QtWidgets.QWidget()
    ui = Ui_trustedData()
    ui.setupUi(trustedData)
    trustedData.show()
    sys.exit(app.exec_())
