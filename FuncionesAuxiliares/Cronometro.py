"""
    https://parzibyte.me/blog
"""
from datetime import datetime
import tkinter as tk
INTERVALO_REFRESCO = 500  # En milisegundos


class Cronometro():

    

    def segundos_a_segundos_minutos_y_horas(self, segundos):
        horas = int(segundos / 60 / 60)
        segundos -= horas*60*60
        minutos = int(segundos/60)
        segundos -= minutos*60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    