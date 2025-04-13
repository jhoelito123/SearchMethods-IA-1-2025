
import tkinter as tk
from tkinter.constants import *
import os.path
import subprocess
_location = os.path.dirname(__file__)

class PresentationFrame:
    def __init__(self, top=None):
        top.geometry("964x648+283+88")
        top.minsize(120, 1)
        top.maxsize(1540, 845)
        top.resizable(1,  1)
        top.title("Problema 1")
        top.configure(background="#F4F1D6")
        self.top = top

        self.btnAsterisco = tk.Button(self.top)
        self.btnAsterisco.place(relx=0.197, rely=0.463, height=56, width=197)
        self.btnAsterisco.configure(activebackground="#F4F1D6")
        self.btnAsterisco.configure(background="#FCF75E")
        self.btnAsterisco.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        self.btnAsterisco.configure(text='''Primero en anchura''', command=lambda: self.open_code(1))

        self.btnOther = tk.Button(self.top)
        self.btnOther.place(relx=0.571, rely=0.463, height=56, width=197)
        self.btnOther.configure(activebackground="#F4F1D6")
        self.btnOther.configure(background="#FCF75E")
        self.btnOther.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        self.btnOther.configure(text='''Otro Algoritmo''')

        self.titleProblem = tk.Label(self.top)
        self.titleProblem.place(relx=0.332, rely=0.0, height=50, width=314)
        self.titleProblem.configure(background="#F4F1D6")
        self.titleProblem.configure(font="-family {Segoe UI Black} -size 20 -weight bold")
        self.titleProblem.configure(text='''Misioneros y canibales''')

        self.descriptionLabel = tk.Label(self.top)
        self.descriptionLabel.place(relx=0.083, rely=0.077, height=170, width=814)
        self.descriptionLabel.configure(background="#F4F1D6")
        self.descriptionLabel.configure(font="-family {Comic Sans MS} -size 13")
        self.descriptionLabel.configure(text='''Tres misioneros y tres caníbales se encuentran en la orilla izquierda de un río que desean cruzar. 
Disponen de una barca con capacidad para transportar como máximo a dos personas. 
Si en algún momento en cualquiera de las orillas hay más caníbales que misioneros
(y al menos un misionero), los caníbales se comerán a los misioneros. El reto consiste en
 encontrar una secuencia de movimientos que permita trasladar a todos los misioneros y 
caníbales a la orilla derecha sin que en ningún momento los misioneros corran peligro.''')

        self.titleProblem_1 = tk.Label(self.top)
        self.titleProblem_1.place(relx=0.28, rely=0.355, height=50, width=434)
        self.titleProblem_1.configure(background="#F4F1D6")
        self.titleProblem_1.configure(font="-family {Segoe UI} -size 15 -weight bold")
        self.titleProblem_1.configure(text='''Seleccione la metodología para la solución:''')

        self.imageProblem = tk.Label(self.top)
        self.imageProblem.place(relx=0.207, rely=0.617, height=221, width=592)
        self.imageProblem.configure(background="#F4F1D6")
        photo_location = os.path.join(_location,"../src/background enormous.png")
        global _img0
        _img0 = tk.PhotoImage(file=photo_location)
        self.imageProblem.configure(image=_img0)
    
    def open_code(self, id):
        if id == 1:
            open_path = os.path.join(os.getcwd(), "Group1", "Asterisco.py")
            if os.path.exists(open_path):
                subprocess.Popen(["python", open_path])
            else:
                print(f"Error: El archivo {open_path} no existe.")
        else:
            print(f"Error: ID {id} no reconocido.") #Logica para abrir el 2do archivo

# Inicializacion de root.
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', root.destroy)
_top1 = root
_w1 = PresentationFrame(_top1)

if __name__ == '__main__':
    root.mainloop()

