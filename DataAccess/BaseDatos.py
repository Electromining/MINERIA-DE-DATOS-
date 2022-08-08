#crear funcion conectar

import sqlite3
#variables
nombreBaseDatos = "DB"

class ConfBaseDatos():
    def __init__(self):
        #self.conectar = sqlite3.connect('/home/pi/Probador-Blower/DataBases/BD.db',check_same_thread=False)
        self.conectar = sqlite3.connect('DataBases/BD.db',check_same_thread=False)        