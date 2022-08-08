import tkinter as tk
from tkinter import ttk
from tkinter import Tk

from PIL import Image, ImageTk

import time
from pySerialTransfer import pySerialTransfer as txfer
import json

import threading

#variables globales
potenciometro = 5
inicio = False


def conectar():
    global potenciometro
    global inicio
    try:
        print("iniciamos")
        link = txfer.SerialTransfer('/dev/ttyACM0')
        #link = txfer.SerialTransfer('/dev/ttyUSB0')
        #link = txfer.SerialTransfer('COM6') # Windows
        #link = txfer.SerialTransfer('/dev/cu.usbmodem92800401')
        
        
        link.open()
        time.sleep(2) # allow some time for the Arduino to completely reset
        ledstate = True
        changetime = time.time()
        senddict = {"ledstate":ledstate}
        while True:
            #check every once in a while to see if it's time to change ledstate     
            if (time.time() - changetime) > 1:
                ledstate = inicio
                changetime = time.time()

            send_size = 0
            send_size = link.tx_obj(ledstate, send_size, val_type_override='?')
            send_size = link.tx_obj(234, send_size, val_type_override='B')

            link.send(send_size)
            # wait for reply to be available 
            while not link.available():
                if link.status < 0:
                    if link.status == txfer.CRC_ERROR:
                        print('ERROR: CRC_ERROR')
                    elif link.status == txfer.PAYLOAD_ERROR:
                        print('ERROR: PAYLOAD_ERROR')
                    elif link.status == txfer.STOP_BYTE_ERROR:
                        print('ERROR: STOP_BYTE_ERROR')
                    else:
                        print('ERROR: {}'.format(link.status))

            rx_struct = {}
            rx_size = 0

            rx_struct['led-state'] = link.rx_obj(obj_type='?', start_pos=rx_size)
            rx_size = txfer.STRUCT_FORMAT_LENGTHS['?']
            rx_struct['some-num'] = link.rx_obj(obj_type=int, start_pos=rx_size)
            rx_size = txfer.STRUCT_FORMAT_LENGTHS['B']

            potenciometro = rx_struct['some-num']
            #print(f"ENVIADO DESDE RASPBERRY: {ledstate}")
            #print(f"RECIBIDO DESDE ARDUINO: potenciometro: {potenciometro}")
  
    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass
    
    except:
        import traceback
        traceback.print_exc()
        
        try:
            link.close()
        except:
            pass

class Aplicacion:
    
    global potenciometro
    global inicio
    def __init__(self):
        
        self.gui=Tk()
        self.gui.title("GTA-41")
        self.gui.geometry('1920x1080')
        #self.gui.attributes('-fullscreen',True)

        #frames
        frame_1 = ttk.Frame(self.gui, height =1080 , width = 1910, borderwidth = 4, relief = 'groove').place(x = 5, y = 5)
        frame_2 = ttk.Frame(frame_1, height = 1080, width = 500, borderwidth = 1, relief = 'groove').place(x = 9, y = 9)

        #logo mecapress
        logo = ImageTk.PhotoImage(Image.open("Recursos/mecapress.png"))
        panel_logo = ttk.Label(frame_1, image = logo, borderwidth = 2, relief = 'groove')
        panel_logo.place(x= 980, y = 25)

        #imagen alternador
        alternador = ImageTk.PhotoImage(Image.open("Recursos/gta-41.png"))
        panel_alternador = ttk.Label(frame_1, image = alternador, borderwidth = 3, relief = 'groove')
        panel_alternador.place(x= 760, y = 200)

        # Etiquetas para las variables
        label_1 = tk.Label(frame_2, bg="#104E8B", fg='white', borderwidth = 2, relief = 'groove')
        label_2 = tk.Label(frame_2, bg="#740937", fg='white', borderwidth = 2, relief = 'groove')
        label_3 = tk.Label(frame_2, bg="#9f1853", fg='white', borderwidth = 2, relief = 'groove')
        label_4 = tk.Label(frame_2, bg="#d02670", fg='white', borderwidth = 2, relief = 'groove')
        label_5 = tk.Label(frame_2, bg="#FFB90F", fg='white', borderwidth = 2, relief = 'groove')
        label_6 = tk.Label(frame_2, bg="#00539a", fg='white', borderwidth = 2, relief = 'groove')
        label_7 = tk.Label(frame_2, bg="#0072c3", fg='white', borderwidth = 2, relief = 'groove')
        label_8 = tk.Label(frame_2, bg="#4589ff", fg='white', borderwidth = 2, relief = 'groove')
        label_9 = tk.Label(frame_2, bg="#EE9A00", fg='white', borderwidth = 2, relief = 'groove')
        label_10 = tk.Label(frame_2, bg="#6929c4", fg='white', borderwidth = 2, relief = 'groove')
        label_11 = tk.Label(frame_2, bg="#8a3ffc", fg='white', borderwidth = 2, relief = 'groove')
        label_12 = tk.Label(frame_2, bg="#a56eff", fg='white', borderwidth = 2, relief = 'groove')
        label_13 = tk.Label(frame_2, bg="#004144", fg='white', borderwidth = 2, relief = 'groove')
        label_14= tk.Label(frame_2, bg="#005d5d", fg='white', borderwidth = 2, relief = 'groove')
        label_15 = tk.Label(frame_2, bg="#CD6600", fg='white', borderwidth = 2, relief = 'groove')
        label_16 = tk.Label(frame_2, bg="#104E8B", fg='white', borderwidth = 2, relief = 'groove')
        label_17= tk.Label(frame_2, bg="#005d5d",fg='white', borderwidth = 2, relief = 'groove')

         # Espacio para los valores de las variables
        #value_1 = tk.Label(frame_2, bg="#33A5FF", borderwidth = 2, relief = 'groove')
        value_2 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_3 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_4 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_5 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_6 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_7 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_8 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_9 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_10 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_11 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_12 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_13 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_14= tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_15 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        value_16 = tk.Label(frame_2, bg="gainsboro", borderwidth = 2, relief = 'groove')
        #value_17= tk.Label(frame_2, bg="#7F7F7F", borderwidth = 2, relief = 'groove')
        
        label_1.place(x=10, y=10, height=67, width=500)
        label_2.place(x=10, y=77, height=67, width=380)
        label_3.place(x=10, y=144, height=67, width=380)
        label_4.place(x=10, y=211, height=67, width=380)
        label_5.place(x=10, y=278, height=67, width=380)
        label_6.place(x=10, y=345, height=67, width=380)
        label_7.place(x=10, y=412, height=67, width=380)
        label_8.place(x=10, y=479, height=67, width=380)
        label_9.place(x=10, y=546, height=67, width=380)
        label_10.place(x=10, y=613, height=67, width=380)
        label_11.place(x=10, y=680, height=67, width=380)
        label_12.place(x=10, y=747, height=67, width=380)
        label_13.place(x=10, y=814, height=67, width=380)
        label_14.place(x=10, y=881, height=67, width=380)
        label_15.place(x=10, y=948, height=67, width=380)
        label_16.place(x=763, y=200, height=60, width=900)
        label_17.place(x=840, y=320, height=50, width=200)
    
        #value_1.place(x=330, y=15, height=45, width=320)
        value_2.place(x=390, y=77, height=67, width=120)
        value_3.place(x=390, y=144, height=67, width=120)
        value_4.place(x=390, y=211, height=67, width=120)
        value_5.place(x=390, y=278, height=67, width=120)
        value_6.place(x=390, y=345, height=67, width=120)
        value_7.place(x=390, y=412, height=67, width=120)
        value_8.place(x=390, y=479, height=67, width=120)
        value_9.place(x=390, y=546, height=67, width=120)
        value_10.place(x=390, y=613, height=67, width=120)
        value_11.place(x=390, y=680, height=67, width=120)
        value_12.place(x=390, y=747, height=67, width=120)
        value_13.place(x=390, y=814, height=67, width=120)
        value_14.place(x=390, y=881, height=67, width=120)
        value_15.place(x=390, y=948, height=67, width=120)
        value_16.place(x=890, y=390, height=50, width=100)
        #value_17.place(x=260, y=735, height=45, width=70)
    

        label_1.config(text="PARAMETROS GTA-41") 
        label_2.config(text="TEMPERATURA 1") 
        label_3.config(text="TEMPERATURA 2") 
        label_4.config(text="TEMPERATURA DISIPADOR\nDE STACK DE POTENCIA") 
        label_5.config(text="CORRIENTE BOBINA\nBOBINA EXCITATRIZ F1-F2") 
        label_6.config(text="CORRIENTE LINEA T1")
        label_7.config(text="CORRIENTE LINEA T2") 
        label_8.config(text="CORRIENTE LINEA T3")
        label_9.config(text="TENSION BOBINA TERCIARIA\nT19-T20 AC") 
        label_10.config(text="TENSION LINEA-LINEA\nT1-T2 AC")
        label_11.config(text="TENSION LINEA-LINEA\nT2-T3 AC") 
        label_12.config(text="TENSION LINEA-LINEA\nT3-T1 AC")
        label_13.config(text="VELOCIDAD DEL ROTOR") 
        label_14.config(text="SALIDA DEL STACK DE POTENCIA F1-F2 DC")  
        label_15.config(text="VIBRACIÓN") 
        label_16.config(text="PROBADOR DINAMOMETRICO GTA-41")
        label_17.config(text="SALIDA DEL STACK") 


        def update_gui():
            """" This function is an update function which is also threaded. The function assimilates the data
            and applies it to it corresponding progress bar. The text box is also updated every couple of seconds.
            A simple auto refresh function .after() could have been used, this has been avoid purposely due to 
            various performance issues.
            """
            global potenciometro
            global inicio
            # while(1):
            #     if inicio == True:
            #         try:
            #             value_16.config(text= potenciometro) 
            #             print("if try statement")
            #         except :
            #             print("temp no")
            #             pass
            #     else:
            #         try:
            #             value_16.config(text= "") 
            #             print("else try statement")
            #         except :
            #             print("temp no")
            #             pass
                

        #threads
        t2 = threading.Thread(target = update_gui)
        t2.daemon = True
        t2.start()

        def start():
            global inicio
            print("Se presiono start ")
            inicio = True
            try:
                value_2.config(text="0.0") 
                value_3.config(text="0.0")
                value_4.config(text="0.0")
                value_5.config(text="0.0")
                value_6.config(text="0.0")
                value_7.config(text="0.0")
                value_8.config(text="0.0")
                value_9.config(text="0.0")
                value_10.config(text="0.0")
                value_11.config(text="0.0")
                value_12.config(text="0.0")
                value_13.config(text="0.0")
                value_14.config(text="0.0")
                value_15.config(text="0.0")
                value_16.config(text="0.0")

            except :
                #print("temp no")
                pass

        def stop():
            global inicio
            print("Se presiono stop ")
            inicio = False
            try:
                value_2.config(text="") 
                value_3.config(text="")
                value_4.config(text="")
                value_5.config(text="")
                value_6.config(text="")
                value_7.config(text="")
                value_8.config(text="")
                value_9.config(text="")
                value_10.config(text="")
                value_11.config(text="")
                value_12.config(text="")
                value_13.config(text="")
                value_14.config(text="")
                value_15.config(text="")
                value_16.config(text="")

            except :
                #print("temp no")
                pass


        #button 
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("TFrame", background="#8f8b8b")
        style.configure('b1.TButton', background = 'darkgreen', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('b1.TButton', background=[('active','darkgreen')])
        style.configure('b2.TButton', background = 'darkred', foreground = 'white', width = 20, borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('b2.TButton', background=[('active','darkred')])

        start = ttk.Button(frame_2, text = "\nSTART\n", width = 30, command = "", style = 'b1.TButton' ).place(x = 870, y = 810)
        stop = ttk.Button(frame_2, text = "\nSTOP\n", width = 30, command = "", style = 'b2.TButton').place(x = 1300, y = 810)
       
 
        self.gui.mainloop()


# if __name__ == "__main__":
    
#     #threads
#     t2 = threading.Thread(target = conectar)
#     t2.daemon = True
#     t2.start()
    
aplicacion1=Aplicacion()