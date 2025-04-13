import tkinter as tk
from tkinter.constants import *
import os.path
import subprocess
_location = os.path.dirname(__file__)

class IndexFrame:
    def __init__(self, top=None):
        top.geometry("992x628+294+117")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(1,  1)
        top.title("Proyecto de Inteligencia Artificial")
        top.configure(background="#9ae1d4")
        self.top = top

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.161, rely=0.828, height=101, width=644)
        self.Label1.configure(background="#9ae1d4")
        self.Label1.configure(font="-family {Segoe Print} -size 11 -slant italic")
        self.Label1.configure(text='''Humberto Alejandro Campos Torrejón          Adam Jhoel Mamani
  Yuri Daniel Ayaviri Quispe               Fabricio Alejandro Herrera Rojas
  Jim Gabriel Ariñez Bautista                 Camila Belen Quispe Flores''')

        self.logoJhoelito = tk.Label(self.top)
        self.logoJhoelito.place(relx=0.06, rely=0.86, height=81, width=78)
        self.logoJhoelito.configure(background="#9ae1d4")
        photo_location = os.path.join(_location,"./src/logoDimensionado.png")
        global _img0
        _img0 = tk.PhotoImage(file=photo_location)
        self.logoJhoelito.configure(image=_img0)

        self.logoSistemas = tk.Label(self.top)
        self.logoSistemas.place(relx=0.817, rely=0.828, height=111, width=110)
        self.logoSistemas.configure(background="#9ae1d4")
        photo_location = os.path.join(_location,"./src/logoSis.png")
        global _img1
        _img1 = tk.PhotoImage(file=photo_location)
        self.logoSistemas.configure(image=_img1)

        self.lblAnya = tk.Label(self.top)
        self.lblAnya.place(relx=-0.02, rely=0.334, height=241, width=256)
        self.lblAnya.configure(background="#9ae1d4")
        photo_location = os.path.join(_location,"./src/imgAnya.png")
        global _img2
        _img2 = tk.PhotoImage(file=photo_location)
        self.lblAnya.configure(image=_img2)

        self.lblTresRaya = tk.Label(self.top)
        self.lblTresRaya.place(relx=0.202, rely=0.271, height=51, width=365)
        self.lblTresRaya.configure(background="#9ae1d4")
        self.lblTresRaya.configure(font="-family {Showcard Gothic} -size 21")
        self.lblTresRaya.configure(text='''Misioneros y Canibales''')

        self.lblMision = tk.Label(self.top)
        self.lblMision.place(relx=0.353, rely=0.51, height=61, width=205)
        self.lblMision.configure(background="#9ae1d4")
        self.lblMision.configure(font="-family {Showcard Gothic} -size 21")
        self.lblMision.configure(text='''Tres en Raya''')

        self.lblTitle = tk.Label(self.top)
        self.lblTitle.place(relx=0.262, rely=0.032, height=50, width=548)
        self.lblTitle.configure(background="#9ae1d4")
        self.lblTitle.configure(font="-family {Segoe Print} -size 30 -weight bold")
        self.lblTitle.configure(text='''Práctica Primer Parcial''')

        self.lblSubtitle = tk.Label(self.top)
        self.lblSubtitle.place(relx=0.373, rely=0.111, height=39, width=292)
        self.lblSubtitle.configure(background="#9ae1d4")
        self.lblSubtitle.configure(font="-family {Segoe Print} -size 13")
        self.lblSubtitle.configure(text='''Metodologías de Búsqueda''')

        self.lblChika = tk.Label(self.top)
        self.lblChika.place(relx=0.726, rely=0.271, height=281, width=266)
        self.lblChika.configure(background="#9ae1d4")
        photo_location = os.path.join(_location,"./src/imgChika.png")
        global _img3
        _img3 = tk.PhotoImage(file=photo_location)
        self.lblChika.configure(image=_img3)

        self.btnG2 = tk.Button(self.top)
        self.btnG2.place(relx=0.565, rely=0.605, height=56, width=157)
        self.btnG2.configure(activebackground="#f9d4db")
        self.btnG2.configure(background="#f9545b")
        self.btnG2.configure(font="-family {Segoe Script} -size 15 -weight bold")
        self.btnG2.configure(text='''Grupo 2''', command= lambda:self.open_group('2'))

        self.btnG1 = tk.Button(self.top)
        self.btnG1.place(relx=0.272, rely=0.382, height=56, width=157)
        self.btnG1.configure(activebackground="#f9d4db")
        self.btnG1.configure(background="#ff9690")
        self.btnG1.configure(font="-family {Segoe Script} -size 15 -weight bold")
        self.btnG1.configure(text='''Grupo 1''', command=lambda:self.open_group('1'))

    def open_group(self, group_number):
        # Concatenar para apuntar al App.py respectivo
        input_data_path = os.path.join(os.getcwd(), f"Group{group_number}", "App.py")

        if os.path.exists(input_data_path):
            subprocess.Popen(["python", input_data_path])
            root.destroy() 
        else:
            print(f"Error: No se encontró el archivo {input_data_path}")
    
# Inicializacion de root.
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', root.destroy)
_top1 = root
_w1 = IndexFrame(_top1)

if __name__ == '__main__':
    root.mainloop()