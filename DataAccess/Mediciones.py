import sqlite3
from datetime import datetime

def obtenerMediciones(cursor):
    result = cursor.execute('SELECT * FROM Mediciones ORDER BY Id ASC')
    labels = result.fetchall()
    return labels

def agregarMediciones(IdPrueba,IdEquipo,IdparametroMedicion,Valor,Tiempo,EstadoDato,cursor,BD):
    date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
    query = "INSERT INTO Mediciones (IdPrueba,IdEquipo,IdparametroMedicion,Valor,Tiempo,Fecha,EstadoDato) VALUES("+str(IdPrueba)+","+str(IdEquipo)+","+str(IdparametroMedicion)+","+str(Valor)+","+str(Tiempo)+",\'"+str(date_time)+"\',"+str(EstadoDato)+");"
    result = cursor.execute(query)
    BD.commit()
    return 0