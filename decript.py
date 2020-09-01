#Maria Jose Castro 181202
#Diana de Leon 18607
#Camila Gonzalez 18398
#Maria Ines Vasquez 18250


#BLOCK CIPHERS
#se esta trabajando con un archivo .TXT

'''
CODIGO REFERNECIADO DE:
https://riptutorial.com/es/python/example/18926/cifrado-simetrico-utilizando-pycrypto#:~:text=El%20algoritmo%20AES%20toma%20tres,un%20vector%20de%20inicializaci%C3%B3n%20aleatorio.
'''

import hashlib
import math
import os

from Crypto.Cipher import AES

IV_SIZE = 16    # Largo de la cadena de 128 bits, estandarizada para el algoritmo AES
KEY_SIZE = 32   # Largo de la llave de 256 bit modificado para el algoritmo AES-256 (32*8=256)
SALT_SIZE = 16  # Tamano recomendado para esta encripccion

#aqui vamos a leer el archivo con el texto encriptado
encriptado = open ('cript.txt','rb')
encrypted = encriptado.read()
encriptado.close()
#contrasena de seguridad
password = input('Ingrese su password segura')
#convertir de texto a bytes
password= str.encode(password)

#accdede al tamano de la sal, y ayuda a encontrar la clave
salt = encrypted[0:SALT_SIZE]
#se genera el vector de inicializacion y la clave del cifrado
derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                              dklen=IV_SIZE + KEY_SIZE)
#vector inicial con tamano 16
iv = derived[0:IV_SIZE]
#llave con tamano 32
key = derived[IV_SIZE:]

#aqui se desencripta el texto
cleartext = AES.new(key, AES.MODE_GCM, iv).decrypt(encrypted[SALT_SIZE:])
#Escribir el archivo con el texto desencriptado
f = open ('text-decripted.txt','wb')
f.write(cleartext)
f.close()
