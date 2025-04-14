
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
        top.title("Problema 2")
        top.configure(background="#e2e2e2")
        self.top = top

        self.btnAsterisco = tk.Button(self.top)
        self.btnAsterisco.place(relx=0.197, rely=0.463, height=56, width=197)
        self.btnAsterisco.configure(activebackground="#e2e2e2")
        self.btnAsterisco.configure(background="#9c9c9c")
        self.btnAsterisco.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        self.btnAsterisco.configure(text='''AlphaBeta''', command=lambda: self.open_code(1))

        self.btnOther = tk.Button(self.top)
        self.btnOther.place(relx=0.571, rely=0.463, height=56, width=197)
        self.btnOther.configure(activebackground="#e2e2e2")
        self.btnOther.configure(background="#9c9c9c")
        self.btnOther.configure(font="-family {Segoe UI Black} -size 12 -weight bold")
        self.btnOther.configure(text='''MiniMax''', command=lambda: self.open_code(2))

        self.titleProblem = tk.Label(self.top)
        self.titleProblem.place(relx=0.332, rely=0.0, height=50, width=314)
        self.titleProblem.configure(background="#e2e2e2")
        self.titleProblem.configure(font="-family {Segoe UI Black} -size 20 -weight bold")
        self.titleProblem.configure(text='''Tres en Raya''')

        self.descriptionLabel = tk.Label(self.top)
        self.descriptionLabel.place(relx=0.083, rely=0.077, height=170, width=814)
        self.descriptionLabel.configure(background="#e2e2e2")
        self.descriptionLabel.configure(font="-family {Comic Sans MS} -size 13")
        self.descriptionLabel.configure(text='''El tres en raya (también conocido como tic-tac-toe o gato) es un juego tradicional
        para dos jugadores que alternan turnos marcando espacios en un tablero de 3×3. Un jugador utiliza
        el símbolo X y el otro O. El objetivo es conseguir alinear tres símbolos iguales en horizontal,
        vertical o diagonal. Si el tablero se llena sin que ningún jugador logre alinear tres símbolos,
        el juego termina en empate.''')

        self.titleProblem_1 = tk.Label(self.top)
        self.titleProblem_1.place(relx=0.28, rely=0.355, height=50, width=434)
        self.titleProblem_1.configure(background="#e2e2e2")
        self.titleProblem_1.configure(font="-family {Segoe UI} -size 15 -weight bold")
        self.titleProblem_1.configure(text='''Seleccione la metodología para la solución:''')

        self.imageProblem = tk.Label(self.top)
        self.imageProblem.place(relx=0.207, rely=0.617, height=221, width=592)
        self.imageProblem.configure(background="#e2e2e2")
        photo_location = os.path.join(_location,"../src/TresEnRayaBG.png")
        global _img0
        _img0 = tk.PhotoImage(file=photo_location)
        self.imageProblem.configure(image=_img0)
    
    def open_code(self, id):
        base_path = os.path.dirname(os.path.abspath(__file__))

        if id == 1:
            open_path = os.path.join(base_path,"TresEnRayaAlphaBeta.py")
        else:
            open_path = os.path.join(base_path,"TresEnRayaMinimax.py")

        if os.path.exists(open_path):
            subprocess.Popen(["python", open_path])
        else:
            print(f"Error: El archivo {open_path} no existe.")


# Inicializacion de root.
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', root.destroy)
_top1 = root
_w1 = PresentationFrame(_top1)

if __name__ == '__main__':
    root.mainloop()