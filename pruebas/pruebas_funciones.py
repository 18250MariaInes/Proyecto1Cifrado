import psycopg2
from config import config
from configmain import configmain
import hashlib
import math
import os
import hashlib

from Crypto.Cipher import AES

from Crypto.Hash import HMAC, SHA256
IV_SIZE = 16    # Largo de la cadena de 128 bits, estandarizada para el algoritmo AES
KEY_SIZE = 32   # Largo de la llave de 256 bit modificado para el algoritmo AES-256 (32*8=256)
SALT_SIZE = 16  # Tamano recomendado para esta encripccion



def signup(username, email, password):#log
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
        master=password
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
        

        hash_user=str.encode(username)

        #aqui se encripta el texto
        encrypted, authTag =  AES.new(key, AES.MODE_GCM, iv).encrypt_and_digest(hash_user)
        # Escribir el archivo con el texto encriptado
        
        #print(authTag)#trustDataCheck PREGUNTAR A SURIANO

        encrypted=salt+encrypted ##sha de diccionario de todos los datos
        encrypted=encrypted 

        cur.execute("INSERT INTO users (username, email, hash_user)VALUES (%s,%s, %s)", (username, email, encrypted))
        conexion.commit()
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def set(name,value, userid):
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
        #print(password)
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
        
        

        encrypted=salt+encrypted
        encrypted=encrypted 

        cur.execute("INSERT INTO passwords (userid, site, password)VALUES (%s,%s, %s)", (userid, name, encrypted))
        conexion.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def init(email, password): #log in
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
        cur.execute("SELECT hash_user FROM users WHERE email=%s", (email,))
        encrypted=cur.fetchall()
        encrypted=encrypted[0][0]
        
        master=password
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

def get(name,master):
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
        
        master=master
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

def getAll(userid):
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
            #print(a,"-",b,"-",c,"-",d)
            dic[c]=d.tobytes()
        print("--------------------------------------------------")      

        #print(dic) 

        cur.close()
        return (dic)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conexion is not None:
            conexion.close()
            print('Conexión finalizada.')

def load(password, representation, trustedDataCheck=None):#comparar con el hash de la sesion anterior paraa verificar integridad
    password=str.encode(password)
    dicc=str.encode(str(representation))
    h = HMAC.new(password, digestmod=SHA256)
    h.update(dicc)
    print(str(h.hexdigest()))
    print(str(trustedDataCheck))
    if (str(h.hexdigest())==str(trustedDataCheck)):
        print("integro")
    else:
        print("lo han hackeado :(")
   
    

def dump(getAll, password):
    password=str.encode(password)
    dicc=str.encode(str(getAll))
    h = HMAC.new(password, digestmod=SHA256)
    h.update(dicc)
    print(h.hexdigest())
    
    
def comprobar(email,password):
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
        cur.execute("SELECT hash_user FROM users WHERE email=%s", (email,))
        encrypted=cur.fetchall()
        encrypted=encrypted[0][0]
        
        master=password
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
        except:
            print("USTED NO PUEDE ENTRAR CON ESE USUARIO")

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
    """set("facebook", "123456",3)
    set("ig", "abcdef",3)
    set("twitter", "123abc",3)
    set("pinterest", "abc123",3)"""
    #get("facebook")
    #remove("facebook")
    #getAll(3)
    #signup("JuanDi", "juan.diego.vf@gmail.com", "abd123")
    #init("juan.diego.vf@gmail.com", "abd123")
    #comprobar("maria.ines.vf@gmail.com", "HOLA")
    #load("maria.ines.vf@gmail.com","soy502",dump())
    #dump(getAll(3),"abd123")
    load("abd123", getAll(3), "75aec25a5d84265542920f19666b3714a762a982d6ed45f8fa7cc98c785a381a")