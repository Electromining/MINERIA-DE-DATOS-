import sqlite3

def obtenerParametrosMediciones(cursor):
    result = cursor.execute('SELECT * FROM ParametrosMediciones ORDER BY Id ASC')
    labels = result.fetchall()
    return labels

