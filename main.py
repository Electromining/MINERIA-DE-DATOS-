# Librerias 
from tkinter import *
import FuncionesAuxiliares.Interfaz as IFZ
#import FuncionesAuxiliares.PuertoSerial as PS

# Funciones
def main():
    try:

        # ----------------- Interfaz ------------------
        root = Tk()
        root.title("Electromining")
        root.geometry('1280x800')
        IFZ.Aplicacion(root) # Call to the App
        root.mainloop()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

    