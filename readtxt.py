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

#aqui vamos a leer el archivo texto plano
archivo = open('text.txt','rb')
cleartext = archivo.read()
#cerramos archivo
archivo.close()
#contrasena de seguridad
password = input('Ingrese su password segura')
#convertir texto de password a bytes
password= str.encode(password)
print(password)
#se genera una cadena de bytes aleatorios (del tamano del salsize)
salt = os.urandom(SALT_SIZE)
#se genera el vector de inicializacion y la clave del cifrado
derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                              dklen=IV_SIZE + KEY_SIZE)
#vector inicial con tamano 16
iv = derived[0:IV_SIZE]
#llave con tamano 32
key = derived[IV_SIZE:]

#aqui se encripta el texto
encrypted, authTag =  AES.new(key, AES.MODE_GCM, iv).encrypt_and_digest(cleartext)
# Escribir el archivo con el texto encriptado

print(authTag)#trustDataCheck PREGUNTAR A SURIANO

encrypted=salt+encrypted
cript = open ('cript.txt','wb')
cript.write(encrypted)
cript.close()

'''
PREGUNTAS

i. ¿Que modo de AES uso? ¿Por que?

Cipher feedback (CFB) y output feedback (OFB)
Estas permiten poder codificar en unidades inferiores al tamano del bloque de
texto. Aprovechado la capacidad de transmision con mayor seguridad.
Este tambien nos proteje con respecto a la sustitucion de bloques.

ii. ¿Que parametros tuvo que hacer llegar desde su funcion de Encrypt a la Decrypt?
¿Porque?
SALT_SIZE
PASSWORD
AES_MODE
IV

Una frase de contraseña no tiene el tamano apropiado ni se debe usar directamente porque
NO es aleatoria, por tanto se usa el algoritmo PBKDF2 para generar un vector de 
inicializacion de 128 bits y una clave de 256 bits a partir de la contraseña

iii. ¿Que variables considera las mas importantes dentro de su implementacion? ¿Por que?

Password: porque esta es la que nos permite encriptar y descencriptar el mismo texto, en el caso
que estas no coincidan en alguno de los pasos el texto a mostrar o encriptar no sera el correcto. 
IV_SIZE: Es el que nos dicta el tamano del vector inicial porque garantiza que la clave generada sea aleatoria.
Salt: este recibe como parametro el sat_size que nos indica el tamano de la cadena, el valor de retorno de OS.RANDOM 
es esta cadena de bytes aleatorios. 

'''
