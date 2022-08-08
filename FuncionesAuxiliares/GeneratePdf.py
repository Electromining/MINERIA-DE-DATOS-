from fpdf import FPDF
from datetime import date
from fpdf.html import hex2dec

class PDF():
    def __init__(self):
        # Cambiamos los margenes
        self.pdf = FPDF('P', 'mm', 'Letter')
        self.pdf.set_left_margin(20)
        self.pdf.set_right_margin(20)
        self.pdf.set_top_margin(20)
        self.pdf.set_top_margin(20)


        # Set auto page break
        self.pdf.add_page()

        self.header()

    def header(self):
        # Logo
        #self.image('Recursos/mecapress.png', 10, 8, 25)
        # Title
        self.pdf.set_font('helvetica', 'B', 20)
        self.pdf.cell(0, 0, 'REPORTE GTA-41', border=False, ln=1, align='C')
        # Line break
        self.pdf.ln(10)
        #date
        self.pdf.set_font('helvetica', '', 15)
        fecha  = date.today().strftime("%b-%d-%Y")
        self.pdf.cell(0, 0, fecha, border=False, ln=1, align='C')
        # Line break
        self.pdf.ln(20)
    
    def data(self,data):
        #data -> [(textoLabel,colorLabel,textoValue,colorValue)]
        #fuente
        self.pdf.set_font('helvetica', 'B', 10)
        for textoLabel,colorLabel,textoValue,colorValue  in data:
            self.pdf.set_text_color(*hex2dec('#ffffff'))
            #padding
            self.pdf.cell(20)
            #text
            self.pdf.set_fill_color(*hex2dec(colorLabel))
            self.pdf.cell(100, 10, textoLabel, ln=0, fill=True, align='C', border=True)
            #value
            self.pdf.set_fill_color(*hex2dec(colorValue))
            self.pdf.cell(40, 10, textoValue, ln=0, fill=True, align='C', border=True) 
            #salto de linea
            self.pdf.ln(h = 10)

    def crear(self,name):
        self.pdf.output(name+'.pdf')







