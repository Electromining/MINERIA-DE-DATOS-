##################### Librerias
import time
import json
from typing import Type

from pySerialTransfer import pySerialTransfer as txfer

######################
# La librreria py serial transfer tiene muy buenas funciones
# https://github.com/PowerBroker2/pySerialTransfer/blob/master/pySerialTransfer/pySerialTransfer.py
##################### Variables Globales


##################### Clases

class PuertoSerial():

    def __init__(self, ledstate):
        # Variables        
        self.rx_struct = dict()
        self.ledstate = ledstate
        self.senddict = {"ledstate":self.ledstate}
        
        # 
        #self.link = txfer.SerialTransfer('/dev/ttyACM0')
        self.link = txfer.SerialTransfer('COM9') # Windows   


    def __del__(self):
        self.link.close()
        print("Terminando PuertoSerial")
    

    def DesconectarSerial(self):
        self.link.close()


    def ConectarSerial(self):
        try:
            # Abre conexión con el puerto serial
            self.link.open()
            time.sleep(2) # allow some time for the Arduino to completely reset     
            print("Serial Conectado")   
        except:
            import traceback
            traceback.print_exc()        
            try:
                self.link.close()
            except:
                pass


    def EnviarSerial(self, data, pararObtenerInformacion):

        #if(pararObtenerInformacion):
        #    print("Thread Parado RECIBIR SENAL")
        #    #cerramos toda conexion con el serial
        #    return 0 

        # Data es una estrucura por lo que accedemos a cada componente
        send_size = 0
        #send_size = self.link.tx_obj(data.test_started, start_pos=send_size)
        send_size = self.link.tx_obj(data.arr_Param, start_pos=send_size)


        print("Enviando...")

        if(self.link.send(send_size)):

            #print("ENVIADO AL ARDUINO: " + 'test_started: '+ str(data.test_started) )
            print("ENVIADO AL ARDUINO: " + 'arr_Param: '+ str(data.arr_Param) )

        else:
            print("---------------------- Error al Enviar ----------------------")



    def RecibirSerial(self, pararObtenerInformacion):



        peso_Packetes = 18
        # Obtenemos la canitidad de packetes mandados
        bytes = self.link.available()
        bytes = bytes/peso_Packetes
        #print("cantidad de paquetes: "+str(bytes))
        if bytes: 
            rx_size = 0
            packets = list()
            for i in range(int(bytes)):

                self.rx_struct['recieve_id'] = self.link.rx_obj(obj_type='l', start_pos=rx_size)
                rx_size += txfer.STRUCT_FORMAT_LENGTHS['l']
                self.rx_struct['potentiometer_value'] = self.link.rx_obj(obj_type='l', start_pos=rx_size)
                rx_size += txfer.STRUCT_FORMAT_LENGTHS['l']
                self.rx_struct['value'] = self.link.rx_obj(obj_type='f', start_pos=rx_size)
                rx_size += txfer.STRUCT_FORMAT_LENGTHS['f']
                #self.rx_struct['etapaPrueba'] = self.link.rx_obj(obj_type='l', start_pos=rx_size)
                #rx_size += txfer.STRUCT_FORMAT_LENGTHS['l']
                self.rx_struct['label'] = self.link.rx_obj(obj_type=str, start_pos=rx_size,obj_byte_size=6).rstrip('\x00')
                rx_size += len(self.rx_struct['label']) + len('\x00')
                
                print(pararObtenerInformacion)
                print(i)
                print("RECIBIDO DESDE ARDUINO:" + str(self.rx_struct))
                
                if(pararObtenerInformacion):
                    print("Thread Parado RECIBIR SENAL")
                    #cerramos toda conexion con el serial
                    return 0
                else:
                    packets.append((self.rx_struct['recieve_id'],self.rx_struct['potentiometer_value'],self.rx_struct['label'],self.rx_struct['value']))
            return packets

        elif self.link.status < 0:
            if self.link.status == txfer.CRC_ERROR:
                print('ERROR: CRC_ERROR')
            elif self.link.status == txfer.PAYLOAD_ERROR:
                print('ERROR: PAYLOAD_ERROR')
            elif self.link.status == txfer.STOP_BYTE_ERROR:
                print('ERROR: STOP_BYTE_ERROR')
            else:
                print('ERROR: {}'.format(self.link.status))
            print('---------------------- Error ----------------------')
            return None
        #print('---------------------- No Data ----------------------')
        return None
                    
                    
            

       
        
                    

    # Esta funcion espera por la rececpcion del puerto serial 
    # probablemente tengamos que cambiar el nombre.
    def ErrorSerial(self):
        self.link.available()
        # while not self.link.available(): # Programar salida alternativa del while 
        #     if self.link.status < 0:
        #         if self.link.status == txfer.CRC_ERROR:
        #             print('ERROR: CRC_ERROR')
        #         elif self.link.status == txfer.PAYLOAD_ERROR:
        #             print('ERROR: PAYLOAD_ERROR')
        #         elif self.link.status == txfer.STOP_BYTE_ERROR:
        #             print('ERROR: STOP_BYTE_ERROR')
        #         else:
        #             print('ERROR: {}'.format(self.link.status))
        #     #print("Error")
        #     time.sleep(2)
        # if not self.link.available(): # Programar salida alternativa del while 
        #     if self.link.status < 0:
        #         if self.link.status == txfer.CRC_ERROR:
        #             print('ERROR: CRC_ERROR')
        #         elif self.link.status == txfer.PAYLOAD_ERROR:
        #             print('ERROR: PAYLOAD_ERROR')
        #         elif self.link.status == txfer.STOP_BYTE_ERROR:
        #             print('ERROR: STOP_BYTE_ERROR')
        #         else:
        #             print('ERROR: {}'.format(self.link.status))