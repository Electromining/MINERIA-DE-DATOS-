import sqlite3
from datetime import datetime

def obtenerPruebas(cursor):
    result = cursor.execute('SELECT * FROM Pruebas')
    pruebas = result.fetchall()
    return pruebas

def cantidadPruebas(cursor):
    result = cursor.execute('SELECT COUNT(*) FROM Pruebas')
    cantidad = result.fetchall()
    return cantidad[0][0]

def añadirPrueba(nombrePrueba,IdUsuario,EstadoPrueba,cursor,BD):
    date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
    print(nombrePrueba)
    query = "INSERT INTO Pruebas (NombrePrueba,IdUsuario,FechaPrueba,EstadoPrueba) VALUES(\'"+str(nombrePrueba)+"\',"+str(IdUsuario)+",\'"+str(date_time)+"\',"+str(EstadoPrueba)+");"
    result = cursor.execute(query)
    BD.commit()
    return 0