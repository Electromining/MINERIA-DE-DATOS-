# Interfaz Probador-GTA-41

## **main\.py**
    Función principal e inicial de la interfaz.
## **Data Access**
    Ruta perteneciente a las funciones de manejo de bases de datos.
## **Data Bases**
    Ruta perteneciente a la base de datos.
## **Funciones Auxiliares**
    Ruta perteneciente a la clase interfaz y generador de PDF. 
## **Recursos**
    Ruta perteneciente a los diferentes archivos auxiliares.

## **Librerias a instalar**

* PIL import Image, ImageTk
sudo apt-get install python3-pil python3-pil.imagetk


* FPDF 
sudo pip3 install fpdf

* SERIAL TRNSFER
sudo pip3 install pySerialTransfer

* IMPRESION

sudo pip3 install adafruit-circuitpython-thermal_printer

CONFIGURACION PUERTOS IMPRESION
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/uart-serial

## **Archivo para el teensy**
    En la carpeta **/teensy** se encuentra el archivo **teensy.ino**, el cual se debe subir a la placa teensy para que funcione la interfaz.
    
## **CONFIGURACION PARA QUE INICIE APLICACION PYTHON AL ENCENDER LA RASPBERRY

* https://noticiasmoviles.com/3-formas-de-ejecutar-un-programa-o-script-de-raspberry-pi-al-inicio/

OPCION 3


Primero, abra la terminal e ingrese el siguiente comando para crear un archivo .desktop en el directorio de inicio automático: sudo nano /etc/xdg/autostart/display.desktop. Usamos display.desktop como el nombre del archivo, pero puedes nombrar tu archivo de escritorio como quieras.

En el archivo .desktop, agregue las siguientes líneas de código:

[Desktop Entry]

Name=PiCounter

Exec=/usr/bin/python3 /home/pi/PiCounter/display.py

En este archivo, sustituya el valor por Nombre propio campo con el nombre del proyecto / script. De manera similar, hemos agregado nuestro programa display.py para que se ejecute cada vez que arranca la Raspberry Pi.
