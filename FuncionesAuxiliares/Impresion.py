import board
import busio

import adafruit_thermal_printer

class Impresion():

    def __init__(self):
        print('inicio impresion')

    def ImprimirPrueba(self, datosInfo, datosMedicion):

        print('prueba')


        #return 0
        
        # Pick which version thermal printer class to use depending on the version of
        # your printer.  Hold the button on the printer as it's powered on and it will
        # print a test page that displays the firmware version, like 2.64, 2.68, etc.
        # Use this version in the get_printer_class function below.
        ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)

        # Define RX and TX pins for the board's serial port connected to the printer.
        # Only the TX pin needs to be configued, and note to take care NOT to connect
        # the RX pin if your board doesn't support 5V inputs.  If RX is left unconnected
        # the only loss in functionality is checking if the printer has paper--all other
        # functions of the printer will work.
        RX = board.RX
        TX = board.TX

        # Create a serial connection for the printer.  You must use the same baud rate
        # as your printer is configured (print a test page by holding the button
        # during power-up and it will show the baud rate).  Most printers use 19200.
        #uart = busio.UART(TX, RX, baudrate=19200)

        # For a computer, use the pyserial library for uart access.
        import serial
        uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=3000)

        # Create the printer instance.
        printer = ThermalPrinter(uart, auto_warm_up=False)

        # Initialize the printer.  Note this will take a few seconds for the printer
        # to warm up and be ready to accept commands (hence calling it explicitly vs.
        # automatically in the initializer with the default auto_warm_up=True).
        printer.warm_up()
        


        printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
        printer.size = adafruit_thermal_printer.SIZE_MEDIUM
        printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
        printer.print('Resultado Prueba Blower')
        # Reset back to normal printing:
        printer.underline = None
        printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
        # Feed lines to make visible:
        printer.feed(4)
        printer.print("")

        printer.underline = None
        printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.print("USUARIO: ", datosInfo[0])
        printer.print("")

        printer.underline = None
        printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.print("FECHA: ", datosInfo[1])
        printer.print("")

        # Print medium size text.
        #printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.print("EQUIPO: ", datosInfo[2])
        printer.print("")



        #printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.print("TIPO DE PRUEBA: ", datosInfo[3])
        printer.print("")

        #printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.print("DURACION:", datosInfo[4])
        printer.print("                                                         ")
        printer.print("                                                         ")
        

        
        #printer.size = adafruit_thermal_printer.SIZE_SMALL
        printer.print("ETAPA 1")
        printer.print("RPM: 500  TIEMPO: 10:00")
        printer.print("------------------------")
        printer.print("Temperatura: " + str(datosMedicion[0]) + " C")
        printer.print("VIBRACION 1: " + str(datosMedicion[1]) + " mm/s")
        printer.print("VIBRACION 2: " + str(datosMedicion[2]) + " mm/s")
        printer.print("VELOCIDAD 1: " + str(datosMedicion[3]) + " RPM")
        printer.print("CORRIENTE 1: " + str(datosMedicion[4]) + " A")
        printer.print("                                                         ")
        printer.print("                                                         ")        
        printer.print("ETAPA 2")
        printer.print("RPM: 1500  TIEMPO: 10:00")
        printer.print("------------------------")
        printer.print("Temperatura: " + str(datosMedicion[5]) + " C")
        printer.print("VIBRACION 1: " + str(datosMedicion[6]) + " mm/s")
        printer.print("VIBRACION 2: " + str(datosMedicion[7]) + " mm/s")
        printer.print("VELOCIDAD 1: " + str(datosMedicion[8]) + " RPM")
        printer.print("CORRIENTE 1: " + str(datosMedicion[9]) + " A")

        if (datosInfo[3] == "Con Carga"):


            printer.print("                                                         ")
            printer.print("                                                         ")
            printer.print("ETAPA 3")
            printer.print("RPM: 2000  TIEMPO: 2:00")
            printer.print("------------------------")
            printer.print("Temperatura: " + str(datosMedicion[10]) + " C")
            printer.print("VIBRACION 1: " + str(datosMedicion[11]) + " mm/s")
            printer.print("VIBRACION 2: " + str(datosMedicion[12]) + " mm/s")
            printer.print("VELOCIDAD 1: " + str(datosMedicion[13]) + " RPM")
            printer.print("CORRIENTE 1: " + str(datosMedicion[14]) + " A")

        if (datosInfo[3] == "Sin Carga"):
            printer.print("                                                         ")
            printer.print("                                                         ")
            printer.print("ETAPA 3")
            printer.print("RPM: 2500  TIEMPO: 10:00")
            printer.print("------------------------")
            printer.print("Temperatura: " + str(datosMedicion[10]) + " C")
            printer.print("VIBRACION 1: " + str(datosMedicion[11]) + " mm/s")
            printer.print("VIBRACION 2: " + str(datosMedicion[12]) + " mm/s")
            printer.print("VELOCIDAD 1: " + str(datosMedicion[13]) + " RPM")
            printer.print("CORRIENTE 1: " + str(datosMedicion[14]) + " A")

            printer.print("                                                         ")
            printer.print("                                                         ")
            printer.print("ETAPA 4")
            printer.print("RPM: 3500  TIEMPO: 2:00")
            printer.print("------------------------")
            printer.print("Temperatura: " + str(datosMedicion[15]) + " C")
            printer.print("VIBRACION 1: " + str(datosMedicion[16]) + " mm/s")
            printer.print("VIBRACION 2: " + str(datosMedicion[17]) + " mm/s")
            printer.print("VELOCIDAD 1: " + str(datosMedicion[18]) + " RPM")
            printer.print("CORRIENTE 1: " + str(datosMedicion[19]) + " A")        
            
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("______________________________")
        printer.print("     FIRMA O VB ENCARGADO     ")                         
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")  
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")
        printer.print("                                                         ")  


        """
        # Print a line of text:
        printer.print("Hello world!")

        # Print a bold line of text:
        printer.bold = True
        printer.print("Bold hello world!")
        printer.bold = False

        # Print a normal/thin underline line of text:
        printer.underline = adafruit_thermal_printer.UNDERLINE_THIN
        printer.print("Thin underline!")

        # Print a thick underline line of text:
        printer.underline = adafruit_thermal_printer.UNDERLINE_THICK
        printer.print("Thick underline!")

        # Disable underlines.
        printer.underline = None

        # Print an inverted line.
        printer.inverse = True
        printer.print("Inverse hello world!")
        printer.inverse = False

        # Print an upside down line.
        printer.upside_down = True
        printer.print("Upside down hello!")
        printer.upside_down = False

        # Print a double height line.
        printer.double_height = True
        printer.print("Double height!")
        printer.double_height = False

        # Print a double width line.
        printer.double_width = True
        printer.print("Double width!")
        printer.double_width = False

        # Print a strike-through line.
        printer.strike = True
        printer.print("Strike-through hello!")
        printer.strike = False

        # Print medium size text.
        printer.size = adafruit_thermal_printer.SIZE_MEDIUM
        printer.print("Medium size text!")

        # Print large size text.
        printer.size = adafruit_thermal_printer.SIZE_LARGE
        printer.print("Large size text!")

        # Back to normal / small size text.
        printer.size = adafruit_thermal_printer.SIZE_SMALL

        # Print center justified text.
        printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER
        printer.print("Center justified!")

        # Print right justified text.
        printer.justify = adafruit_thermal_printer.JUSTIFY_RIGHT
        printer.print("Right justified!")

        # Back to left justified / normal text.
        printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT
        """
        





