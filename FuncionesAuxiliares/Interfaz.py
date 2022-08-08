# ---------------------------------- Librerias ----------------------------------
#Librerias basicas
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import threading
from datetime import datetime

import requests
import json

#librerias temporales
from random import random
from random import randint

#Librerias locales
import DataAccess.BaseDatos as CNBD
import DataAccess.Mediciones as DAM
import DataAccess.Labels as Labels
import DataAccess.Pruebas as DAP
import FuncionesAuxiliares.GeneratePdf as GeneratePdf
import FuncionesAuxiliares.PuertoSerial as PS
import FuncionesAuxiliares.Cronometro as Crono
#import FuncionesAuxiliares.Impresion as Impresion
# ---------------------------------- Variables ----------------------------------

#conexiones base de datos
baseDatos = CNBD.ConfBaseDatos().conectar
cursor = baseDatos.cursor() 

#conexiones RP
serial = PS.PuertoSerial(True)

#labels
labelsData = {}

#CRONOMETRO
crono = Crono.Cronometro()

#IMPRESION
#impresion = Impresion.Impresion()

datosInfo = []
datosMedicionConCarga = [
        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0       
]

rpmInfoConCarga = ['0', '500','1500','2000']
rpmInfoSinCarga = ['0', '500','1500','2500','3500']

tiempoPruebaTotal = '0'

#Inicio de prueba
inicioPrueba = 0
startClock = False

#obtenerinformacio
tiempoObtencion = 0.01   
pararObtenerInformacion = False
obtenerInforamcionThread = 0

#prueba
IdPrueba = 0

resWidth = 1280
resHeigth = 800


etapaGlobal = 0

class Aplicacion():

    def __init__(self,root):
        
        # ---------------------------------- Funciones ----------------------------------
        serial.ConectarSerial()

        #Obtenemos los labels de la base de datos
        def getLabels():
            
            posIniX = 20
            posIniY = 150
            
            altoLabels = 30
            

            labels = Labels.obtenerParametrosMediciones(cursor)
            for e,label in enumerate(labels):
                id = label[0]
                idEquipo = label[1]
                nombreParametro = label[2]
                idTipo = label[3]
                colorFondo = label[4]
                colorFuente = label[5]
                Estado = label[6]

                #NOMBRE DE PARAMETROS
                label = tk.Label(frame_2, bg = colorFondo, fg = 'white', borderwidth = 3, relief = 'ridge', text = nombreParametro, font='Helvetica 10 bold')
                label.place(x = posIniX + 30, y = posIniY + altoLabels + e * altoLabels, height = altoLabels, width = 300)

                #VALORES PARAMETROS
                value = tk.Label(frame_2, bg = "#DCDCDC", borderwidth = 3, relief = 'ridge', text = '-', font='Helvetica 10 bold')
                value.place(x = posIniX + 330, y = posIniY + altoLabels + e * altoLabels, height = altoLabels, width = 150)

                labelsData[str(id)] = (label,value)
        
        #Iniciamos una prueba
        def startPrueba():


            #serial.ConectarSerial()

            #idprueba -> incremental por c/p

            #variables
            global startClock
            global inicioPrueba
            global obtenerInforamcionThread
            global pararObtenerInformacion
            global IdPrueba
            global etapaGlobal


            etapaGlobal = 0

            startTestPi = 1 #variable que controla el inicio de la prueba y la envia al teensy
            '''
            if (usuarioEntry.get() == '' or comboAspa.get() == ''):
                messagebox.showinfo(message="Debe completar los datos de Usuario, Equipo y Prueba", title="Título")
                return 0
            '''

            #AgregarDatosInfo()
            
            #funcion
            #print("Inicio de prueba")

            #configuramos y añadimos el valor de una prueba
            IdPrueba = DAP.cantidadPruebas(cursor)+1
            DAP.añadirPrueba("Prueba "+str(IdPrueba),1,1,cursor,baseDatos)

            #configuramos el inicio del contador
            startClock = True
            inicioPrueba = time.time()
            clock()

            #configuramos los labels
            #tensionValue.config(state=tk.DISABLED)
            #tiempoValue.config(state=tk.DISABLED)

            
            for label in labelsData:
                labelsData[label][1].config(text = "0")

            
            #iniciamos la obtencion de la informacion
            time.sleep(1)
            #creamos un tread para obtner la informacion en paralelo
            pararObtenerInformacion = False
            obtenerInforamcionThread = threading.Thread(target = obtenerInformacion)
            obtenerInforamcionThread.start()
            print('Thread Creado MEDICIONES TEENSY')
            
    
            #configuramos los botones
            start.state(["disabled"]) 
            stop.state(["!disabled"]) 
            #reporte.state(["disabled"]) 


            if (comboAspa.get() == "Con Carga"):
                parametroCarga = 2
            else:
                parametroCarga = 1

            # Comenzamos la prueba en el teensy
            # Creamos la estructura para enviarla
            class struct(object):
                #test_started = True
                arr_Param = [int(startTestPi), parametroCarga]

            SendStruct = struct

            # Enviamos la estructura 
            serial.EnviarSerial(SendStruct, pararObtenerInformacion)


        def AgregarDatosInfo():
            
            datosInfo.clear()
            #datosInfo.insert(0,usuarioEntry.get())
            datosInfo.insert(1, datetime.today().strftime('%d-%m-%Y %H:%M'))
            #datosInfo.insert(2, equipoEntry.get())
            datosInfo.insert(3, comboAspa.get())
            #datosInfo.insert(4, tiempoPruebaTotal) #obtengo la duracion de la prueba

        #Paramos una prueba
        def stopPrueba():

        

            #variables
            global startClock
            global obtenerInforamcionThread
            global pararObtenerInformacion
            global etapaGlobal

            etapaGlobal = 0

            startTestPi = 0 #variable que controla el final de la prueba y la envia al teensy
            
            datosInfo.insert(4, tiempoPruebaTotal) #obtengo la duracion de la prueba
            #AgregarDatosInfo()
            #print(datosInfo)
            print("stop")

            startClock = False

            #CAMBIAMOS LA VARIABLE DE EJECUCION Del thread
            pararObtenerInformacion = True

            if (comboAspa.get() == "Con Carga"):
                parametroCarga = 2
            else:
                parametroCarga = 1
            # Comenzamos la prueba en el teensy
            # Creamos la estructura para enviarla
            class struct(object):
                #test_started = False
                arr_Param = [int(startTestPi), parametroCarga]

            SendStruct = struct

            # Enviamos la estructura 
            serial.EnviarSerial(SendStruct, pararObtenerInformacion)

            #configuramos los labels
            #tensionValue.config(state=tk.NORMAL)
            #tiempoValue.config(state=tk.NORMAL)

            for label in labelsData:
                labelsData[label][1].config(text = format(0, ".1f"))
            
            #tensionActualValue.config(text='0')


            #configuramos los botones
            start.state(["!disabled"]) 
            
            stop.state(["disabled"]) 
            #reporte.state(["!disabled"])  
            
            # TO DO "REVISAR THREAD https://es.acervolima.com/python-diferentes-formas-de-matar-un-hilo/"
            
            #print("Termino de una prueba")
            #detenemos el thread            

            
            #time.sleep(3)
            messagebox.showinfo(message="Prueba Finalizada", title="Mensaje")
            #obtenerInforamcionThread.join()
            
            #serial.DesconectarSerial()

                    
        #Creamos un reporte
        def crearReporte():
            #variables
            global labelsData
            #lista de informacion
            data = list()

            #creamos la data
            for key in labelsData:
                text,value = labelsData[key]
                # print(text.cget("text"))
                # print(text.cget("bg"))
                # print(value.cget("text"))
                # print(value.cget("bg"))
                data.append((text.cget("text"),text.cget("bg"),value.cget("text"),value.cget("bg")))
                

            # Create a PDF object
            pdf = GeneratePdf.PDF()
            pdf.data(data)
            pdf.crear("Reporte")
            
        
        #Relog
        def clock():
            #variables
            global startClock
            global inicioPrueba
            global tiempoPruebaTotal

            #funcion
            if(startClock):
                segundos = time.time() - inicioPrueba
                tiempoActualValue.config(text=crono.segundos_a_segundos_minutos_y_horas(int(segundos)))
                tiempoPruebaTotal = crono.segundos_a_segundos_minutos_y_horas(int(segundos))
            else:
                tiempoActualValue.config(text=crono.segundos_a_segundos_minutos_y_horas(int(0)))
                #tiempoPruebaTotal=crono.segundos_a_segundos_minutos_y_horas(int(0))
            tiempoActualValue.after(500,clock)

        #obtenemos la informacion THREAD
        def obtenerInformacion():
            global IdPrueba
            global serial 
            global etapaGlobal
            etapaGlobal = 0
            led_status = True
            idPacket = 0

            global tiempoEnvio
            global tiempoEnvioTranscurrido
            global contadorMediciones
            global swSubirMediciones

            swSubirMediciones = False
            tiempoEnvioTranscurrido = 0
            tiempoEnvio = 2
            contadorMediciones = 0

            while(True):


                



                cantidadMediciones = 0
                
                if(pararObtenerInformacion):
                    #print("Thread Parado")
                    #cerramos toda conexion con el serial
                    return 0
                    
                else:

                    received = serial.RecibirSerial(pararObtenerInformacion)
                    
                    if(pararObtenerInformacion):
                        #print("Thread Parado")
                        #cerramos toda conexion con el serial
                        return 0

                    # Si obtenemos un dato realizamos un cambio en la interfaz
                    if received:




                        #print('received')
                        #print(received)
                        for recieve_id,potentiometer_value,label,value in received:

                            if  (tiempoEnvioTranscurrido > tiempoEnvio ):
                                swSubirMediciones = True
                                print('-----------------------------------------------------------------------------SUBIR DATOS-----------------------------------------------------------')
                                print(label.split("-")[0])
                                print(format(value, "."+str(label.split("-")[1])+"f"))
                                fechaNuevaMedicion = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')
                                print(fechaNuevaMedicion)
                                
                                #SubirMediciones(label.split("-")[0], format(value, "."+str(label.split("-")[1])+"f"), fechaNuevaMedicion)

                                if (contadorMediciones > 5):
                                    contadorMediciones = 0
                                    swSubirMediciones = False        
                                    tiempoEnvioTranscurrido = 0
                                else:
                                    contadorMediciones = contadorMediciones + 1
                            else:
                                tiempoEnvioTranscurrido = tiempoEnvioTranscurrido + tiempoObtencion

                            print(tiempoEnvioTranscurrido)                            

                            if label != "000-0":


                                #actualizamos el label de la tension
                                tensionActualValue.config(text= potentiometer_value)

                                # Actualizamos el listado de parametros, label().split("-")[0] = CODIGO MEDICION, label().split("-")[1] = CANTIDAD DECIMALES
                                labelsData[label.split("-")[0]][1].config(text = format(value, "."+str(label.split("-")[1])+"f"))


                                # Mostramos el label cambiado
                                #print("Label actualizado:",labelsData[label.split("-")[0]][0].cget("text"))
                                
                                '''
                                if (etapa != 10 and etapa != 0 ):

                                    idMedicionEtapa = (str(etapa)+'-'+str(label))
                                    #CrearDataMediciones(value, idMedicionEtapa)
                                    cantidadMediciones = cantidadMediciones + 1
                                    print(cantidadMediciones)
                                '''
                                #if (label == '401-1' and value == 0 ):
                                #messagebox.showinfo(message="Prueba Finalizada", title="Mensaje")
                                #stopPrueba()

                                    #messagebox.showinfo(message="Prueba Finalizada", title="Mensaje")
                                #seccionLabel.config(text='Etapa: ' + str(etapa))
                                '''
                                if (etapa != 10 and etapa != 0 ):

                                    if (comboAspa.get() == "Con Carga"):
                                        rpmLabel.config(text=rpmInfoConCarga[etapa] + '\nRPM')
                                    else:
                                        rpmLabel.config(text=rpmInfoSinCarga[etapa] + '\nRPM')
                                '''        
                                #else:
                                #    etapa = 0
                                #    rpmLabel.config(text='0\nRPM')                                    

                                '''
                                if (etapaGlobal == 10 ):

                                    stopPrueba()
                                else:
                                    etapaGlobal = etapa
                                '''
                                # Subimos la data a la base de datos
                                #IdPrueba,IdEquipo,IdparametroMedicion,Valor,Tiempo,Fecha,EstadoDato
                                #DAM.agregarMediciones(IdPrueba,1,label,value,str(time.time() - inicioPrueba),1,cursor,baseDatos)
                        
                        

                    #damos un tiempo entre cada llamada
                    time.sleep(tiempoObtencion)
        

        def PrintPrueba():
            print('')
            #impresion.ImprimirPrueba(datosInfo, datosMedicionConCarga)

        # ---------------------------------- Interfaz ----------------------------------

        def CrearDataMediciones(valorMedicion, idMedicion):

            diccionarioDatosMedicionConCarga = [
                '1-100-1',
                '1-601-1',
                '1-602-1',
                '1-401-1',
                '1-201-1',
                '2-100-1',
                '2-601-1',
                '2-602-1',
                '2-401-1',
                '2-201-1',
                '3-100-1',
                '3-601-1',
                '3-602-1',
                '3-401-1',
                '3-201-1',
                '4-100-1',
                '4-601-1',
                '4-602-1',
                '4-401-1',
                '4-201-1'
            ]



            indiceCambioValor = diccionarioDatosMedicionConCarga.index(idMedicion)

            datosMedicionConCarga.pop(indiceCambioValor)
            datosMedicionConCarga.insert(indiceCambioValor, valorMedicion)
            #print(datosMedicionConCarga)


        def SubirMediciones(idMedicion, valorMedicion, fechaMedicion):
                
            response = requests.post(
                'https://apimotoresdc.azurewebsites.net/api/Mediciones',
                json={
                    "IdSensor": 1,
                    "IdEquipo": 1,
                    "IdTipoMedicion": int(idMedicion),
                    "Valor": float(valorMedicion),
                    "FechaRegistro": fechaMedicion
                    }

                )

                
            print('Status code: ', response.status_code)
            print('Respuesta desde el servidor:')
            print(response.json())

        xAjustePos = 10

        #root
        self.gui = root

        s = ttk.Style()
        s.theme_use('alt')
        s.configure('new.TFrame', background='#024A86',focuscolor='none')

        idcolor = StringVar(value=1)

        #frames
        frame_1 = ttk.Frame(self.gui, height =1080 , width = 1420, borderwidth = 1, relief = 'groove', style="new.TFrame").place(x = 0, y = 0)
        frame_2 = ttk.Frame(self.gui, height = 250, width = 450, borderwidth = 0, relief = 'groove',style="new.TFrame").place(x =670 , y = 220)

        #imagen equipo
        
        #alternadorPhoto = ImageTk.PhotoImage(Image.open("/home/pi/Probador-MotoresDC/Recursos/Equipo.png"))
        #alternadorPhoto = ImageTk.PhotoImage(Image.open("Recursos/Equipo.png"))

        #alternadorLabel = ttk.Label(frame_1, image = alternadorPhoto, borderwidth = 0, relief = 'groove')
        #alternadorLabel.image = alternadorPhoto 
        #alternadorLabel.place(x= xAjustePos + 40, y = 220)

        #logo mecapress
        #logoPhoto = ImageTk.PhotoImage(Image.open("/home/pi/Probador-MotoresDC/Recursos/logo.png"))
        logoPhoto = ImageTk.PhotoImage(Image.open("Recursos/logo.png"))

        logoLabel = ttk.Label(frame_1, image = logoPhoto, borderwidth = 0, relief = 'groove')
        logoLabel.image = logoPhoto 
        logoLabel.place(x= xAjustePos + 40, y = 70)

        #logo secundario
        #logoPhoto = ImageTk.PhotoImage(Image.open("/home/raspberry/Documentos/Probador-MotoresDC/Recursos/logoSecundario.png"))
        #logoPhoto = ImageTk.PhotoImage(Image.open("Recursos/logoSecundario.png"))

        #logoLabel = ttk.Label(frame_1, image = logoPhoto, borderwidth = 0)
        #logoLabel.image = logoPhoto 
        #logoLabel.place(x= xAjustePos + 970, y = 600)
        

        #logo corfo
        #logoPhoto = ImageTk.PhotoImage(Image.open("/home/pi/Probador-MotoresDC/Recursos/logoSecundario.png"))
        logoPhoto = ImageTk.PhotoImage(Image.open("Recursos/logoCorfo.png"))

        logoLabel = ttk.Label(frame_1, image = logoPhoto, borderwidth = 0)
        logoLabel.image = logoPhoto 
        logoLabel.place(x= xAjustePos + 1140, y = 640)

        #logo orbcomm
        #logoPhoto = ImageTk.PhotoImage(Image.open("/home/pi/Probador-MotoresDC/Recursos/logoOrbcomm.png"))
        #logoPhoto = ImageTk.PhotoImage(Image.open("Recursos/logoOrbcomm.png"))

        #logoLabel = ttk.Label(frame_1, image = logoPhoto, borderwidth = 0)
        #logoLabel.image = logoPhoto 
        #logoLabel.place(x= xAjustePos + 770, y = 210)

        #TITULO PARAMETROS      
        #headingLabel = tk.Label(frame_2, bg="#666666", fg='#FFFFFF', borderwidth = 2, relief = 'groove', text = "PARÁMETROS", font='Helvetica 14 bold')
        #headingLabel.place(x=700, y=270, height=50, width=450)

    
        #TITULO
        probadorLabel = tk.Label(frame_1, bg="#999999", fg='white', borderwidth = 2, relief = 'groove',text='Kit Sensórica', font='Helvetica 16 bold')
        probadorLabel.place(x=0, y=0, height=50, width=resWidth)

        #botones ESTILO
        style = ttk.Style()
        style.configure("TFrame", background="#8f8b8b")
        style.configure('b1.TButton', background = 'green', foreground = 'white', width = 15, heigth = 40, borderwidth=1, focusthickness=1, focuscolor='none', font='Helvetica 16 bold')
        style.configure('b2.TButton', background = 'red', foreground = 'white', width = 15, borderwidth=1, focusthickness=3, focuscolor='none', font='Helvetica 16 bold')
        style.configure('b3.TButton', background = 'gray', foreground = 'white', width = 15, borderwidth=1, focusthickness=3, focuscolor='none', font='Helvetica 16 bold')
        style.configure('b4.TButton', background = '#FFFFFF', foreground = '#104E8B', width = 20, borderwidth=1, focusthickness=3, focuscolor='none', font='Helvetica 16 bold')

        #BOTONES START STOP IMPRIMIR
        start = ttk.Button(frame_1, text = "\nSTART\n", command = startPrueba, style = 'b1.TButton' )
        start.place(x = xAjustePos + 40, y = 640)
        stop = ttk.Button(frame_1, text = "\nSTOP\n", command = stopPrueba, style = 'b2.TButton', state='disabled')
        stop.place(x = xAjustePos + 300, y = 640)

        #btnPrint = ttk.Button(frame_1, text = "\nPRINT\n", command = PrintPrueba, style = 'b4.TButton')
        #btnPrint.place(x = xAjustePos + 680, y = 600)

        #INFO RPM y SECCION


        #seccionLabel = tk.Label(frame_1, bg="#999999", fg='white', borderwidth = 2, relief = 'groove',text='Etapa: 0', font='Arial 14 bold')
        #seccionLabel.place(x=600, y=220, height=100, width=100)

        #rpmLabel = tk.Label(frame_1, bg="#999999", fg='white', borderwidth = 2, relief = 'groove',text='0\n RPM', font='Helvetica 14 bold')
        #rpmLabel.place(x=600, y=320, height=150, width=100)
        # reporte = ttk.Button(frame_1, text = "\nGENERAR REPORTE\n", width = 30, command = crearReporte, style = 'b3.TButton', state='disable')
        # reporte.place(x=1540, y=640, height=50, width=334)



        #tiempo Label
        # tiempoLabel = tk.Label(frame_1, bg="#005d5d",fg='white', borderwidth = 2, relief = 'groove', text="TIEMPO")
        # tiempoLabel.place(x=1520, y=360, height=50, width=167)
        # tiempoValue = ttk.Entry(frame_1, justify=tk.CENTER, font='Helvetica 15')
        # tiempoValue.place(x=1730, y=360, height=50, width=167)

        #separador
        #separadorLabel = tk.Label(frame_1, bg="#104E8B",fg='white', borderwidth = 2, relief = 'groove')
        #separadorLabel.place(x=610, y=300, height=10, width=395)

        #valores de control

        xjustePosDatos = 165

        #Usuario
        #usuarioLabel = tk.Label(frame_1, bg = "#666666",fg = '#FFFFFF', borderwidth = 1, relief = RAISED, text = "Usuario:" , font='Helvetica 12 bold', anchor='w')
        #usuarioLabel.place(x= xAjustePos + xjustePosDatos + 340, y=70, height=30, width=320)

        #usuarioEntry = tk.Label(frame_1, bg = "#666666",fg = '#FFFFFF', borderwidth = 1, relief = RAISED, text='Exponor 2022', font='Helvetica 14 bold', anchor='w')
        #usuarioEntry.place(x= xAjustePos + xjustePosDatos + 340, y=100, height=40, width=320)
        
        #combo implementar despues
        #selectUsuarios = tk.StringVar()
        #comboUsuarios = ttk.Combobox(frame_1, textvariable=selectUsuarios, state="readonly" , font='Helvetica 10 bold')
        #comboUsuarios['values'] = ['Ximena Baeza', 'Gustavo Concha', 'Karlyn Gutierrez']
        #comboUsuarios.place(x= xAjustePos + 300, y=90, height=30, width=170)


        #equipo
        """
        equipoLabel = tk.Label(frame_1, bg = "#CCCCCC",fg = '#000000', borderwidth = 1, relief = RAISED, text = "Equipo:" , font='Helvetica 12 bold', anchor='w')
        equipoLabel.place(x = xAjustePos + xjustePosDatos + 470, y = 70, height = 20, width = 170)

        equipoEntry = ttk.Entry(frame_1, justify=tk.CENTER, font='Helvetica 12')
        equipoEntry.place(x = xAjustePos + xjustePosDatos + 470, y = 90, height = 30, width = 170)
        """

        #combo implementar despues
        #selecEquipos = tk.StringVar()
        #comboEquipos = ttk.Combobox(frame_1, textvariable=selecEquipos, state="readonly" , font='Helvetica 10 bold')
        #comboEquipos['values'] = ['Blower 338-k', 'Blower 485-W', 'Blower 787-U']
        #comboEquipos.place(x= xAjustePos + 470, y=90, height=30, width=170)


        #VELOCIDAD
        aspaLabel = tk.Label(frame_1, bg = "#666666",fg = '#000000', borderwidth = 1, relief = RAISED, text = "Velocidad %" , font='Helvetica 12 bold')
        aspaLabel.place(x= xAjustePos + xjustePosDatos + 660, y=70, height=30, width=150)

        
        selecAspa = tk.StringVar()
        comboAspa = ttk.Combobox(frame_1, textvariable=selecAspa, state="readonly", justify=tk.CENTER , font='Helvetica 14 bold')
        comboAspa['values'] = [0, 50, 75, 100]
        comboAspa.place(x= xAjustePos + xjustePosDatos + 660, y=100, height=40, width=150)

        
        #tensionValue = ttk.Entry(frame_1, justify=tk.CENTER, font='Helvetica 10 bold')
        #tensionValue.place(x= xAjustePos + 300, y=90, height=30, width=200)

        #potencia actual Label
        #tensionActualLabel = tk.Label(frame_1, bg="#FFFFFF",fg = '#000000', borderwidth = 2, relief = 'groove', text="NIVEL DE TENSION DE\nSALIDA TRIFASICA ACTUAL", font='Helvetica 11 bold')
        #tensionActualLabel.place(x= xAjustePos + 810, y=130, height=50, width=240)
        tensionActualValue = tk.Label(frame_1, bg="#FFFFFF", borderwidth = 0, relief='flat', text="-", font='Helvetica 16 bold')
        tensionActualValue.place(x= xAjustePos + 220, y=400, height=50, width=140)

        #tiempo actual Label
        tiempoActualLabel = tk.Label(frame_1, bg="#666666",fg = '#000000', borderwidth = 2, relief = RAISED, text="Tiempo Prueba:", font='Helvetica 12 bold')
        tiempoActualLabel.place(x= xAjustePos + xjustePosDatos + 810, y=70, height=30, width=160)
        tiempoActualValue = tk.Label(frame_1, bg="gainsboro", borderwidth = 2, relief = 'groove',text="-", font='Helvetica 14 bold')
        tiempoActualValue.place(x= xAjustePos + xjustePosDatos + 810, y=100, height=40, width=160)



        #Creamos los Labes correspondiente a cada variable
        getLabels()
        #Iniciamos el relog
        clock()


