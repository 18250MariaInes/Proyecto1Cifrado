import psycopg2
from config import config
import hashlib
import math
import os

from Crypto.Cipher import AES
IV_SIZE = 16    # Largo de la cadena de 128 bits, estandarizada para el algoritmo AES
KEY_SIZE = 32   # Largo de la llave de 256 bit modificado para el algoritmo AES-256 (32*8=256)
SALT_SIZE = 16  # Tamano recomendado para esta encripccion


def set(name,value):
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
        master="hola"
        password= str.encode(master)
        print(password)
        #se genera una cadena de bytes aleatorios (del tamano del salsize)
        
        salt = os.urandom(SALT_SIZE)
        derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                                  dklen=IV_SIZE + KEY_SIZE)
        
        #vector inicial con tamano 16
        iv = derived[0:IV_SIZE]
        #llave con tamano 32
        key = derived[IV_SIZE:]
        

        value=str.encode(value)

        #aqui se encripta el texto
        encrypted, authTag =  AES.new(key, AES.MODE_GCM, iv).encrypt_and_digest(value)
        # Escribir el archivo con el texto encriptado
        
        print(authTag)#trustDataCheck PREGUNTAR A SURIANO

        encrypted=salt+encrypted
        encrypted=encrypted 

        cur.execute("INSERT INTO passwords (userid, site, password)VALUES (%s,%s, %s)", (2, name, encrypted))
        conexion.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')


def get(name):
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
        cur.execute("SELECT password FROM passwords WHERE userid=%s and site=%s", (2, name))
        encrypted=cur.fetchall()
        encrypted=encrypted[0][0]
        
        master="hola"
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

def remove(name):
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
        cur.execute("DELETE FROM passwords WHERE passwords.userid = %s AND passwords.site=%s",(2,name))
        conexion.commit()      

        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')




def conectar():
    """ Conexión al servidor de pases de datos PostgreSQL """
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

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')



if __name__ == '__main__':
    #set("facebook", "123456")
    #get("facebook")
    #remove("facebook")