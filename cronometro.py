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

    def obtener_tiempo_transcurrido_formateado(self):
        segundos_transcurridos= (datetime.now() - hora_inicio).total_seconds()
        return crono.segundos_a_segundos_minutos_y_horas(int(segundos_transcurridos))


    def refrescar_tiempo_transcurrido(self):
        print("Refrescando!")
        variable_hora_actual.set(crono.obtener_tiempo_transcurrido_formateado())
        raiz.after(INTERVALO_REFRESCO, crono.refrescar_tiempo_transcurrido)
    

if __name__ == '__main__':
    raiz = tk.Tk()
    crono = Cronometro()
    hora_inicio = datetime.now()
    variable_hora_actual = tk.StringVar(raiz, value=crono.obtener_tiempo_transcurrido_formateado())

    raiz.etiqueta = tk.Label(raiz, textvariable=variable_hora_actual, font=f"Consolas 60")
    raiz.etiqueta.pack(side="top")
    app = tk.Frame()
    raiz.title("Cronómetro con Tkinter - By Parzibyte")
    crono.refrescar_tiempo_transcurrido()
    app.pack()
    app.mainloop()
