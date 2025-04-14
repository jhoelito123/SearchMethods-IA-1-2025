import heapq
import tkinter as tk

class Node:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = self.heuristic()
        self.f = self.g + self.h

    def heuristic(self):
        c, m, _, _, _ = self.state
        return (c + m) / 2

    def __lt__(self, other):
        return self.f < other.f

    def is_valid(self):
        c_izq, m_izq, _, c_der, m_der = self.state
        if not (0 <= c_izq <= 3 and 0 <= m_izq <= 3 and 0 <= c_der <= 3 and 0 <= m_der <= 3):
            return False
        if m_izq > 0 and c_izq > m_izq:
            return False
        if m_der > 0 and c_der > m_der:
            return False
        return True

    def is_goal(self):
        return self.state == (0, 0, 1, 3, 3)

    def get_children(self):
        children = []
        moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]
        c, m, boat, c_r, m_r = self.state

        for dc, dm in moves:
            if boat == 0:
                new_state = (c - dc, m - dm, 1, c_r + dc, m_r + dm)
            else:
                new_state = (c + dc, m + dm, 0, c_r - dc, m_r - dm)

            child = Node(new_state, parent=self, g=self.g + 1)
            if child.is_valid():
                children.append(child)
        return children

    def get_path(self):
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]

def astar():
    start = Node((3, 3, 0, 0, 0))
    open_set = []
    heapq.heappush(open_set, start)
    visited = set()

    while open_set:
        current = heapq.heappop(open_set)

        if current.state in visited:
            continue
        visited.add(current.state)

        if current.is_goal():
            return current.get_path()

        for child in current.get_children():
            if child.state not in visited:
                heapq.heappush(open_set, child)
    return None


class App:
    def __init__(self, root, path):
        self.root = root
        self.root.title("A* - Misioneros y Caníbales")
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Left Panel
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True)

        self.descripcion = tk.Label(left_frame, text="""Estados: Cualquier tupla (Ci, Mi, B, Cd, Md) donde:
-> Mi, Ci: número de misioneros y caníbales en la orilla izquierda
-> B: posición de la barca (0 = izquierda, 1 = derecha)
-> Md, Cd: número de misioneros y caníbales en la orilla derecha
Acciones:
* Cruzar 1 misionero
* Cruzar 1 caníbal
* Cruzar 2 misioneros
* Cruzar 2 caníbales
* Cruzar 1 misionero y 1 caníbal
Test Objetivo: Alcanzar el estado (0, 0, 1, 3, 3)
Costo Ruta: Cada acción (cruce del río) tiene costo 1.
""",
                                    font=("-family {Comic Sans MS} -size 13"), wraplength=450, justify="left", bg="#F4F1D6")
        self.descripcion.pack(fill="x")

        # Grafico
        self.canvas = tk.Canvas(left_frame, width=700, height=300, bg="#F4F1D6")
        self.canvas.pack()

        # Right panel
        right_frame = tk.Frame(main_frame, bg="#FCF75E", bd=2, relief="sunken")
        right_frame.pack(side="right", fill="y", expand=False)
        tk.Label(right_frame, text="Esquema de Estados A*", font=("Arial", 12, "bold"), bg="#FCF75E").pack(pady=5)
        tk.Label(right_frame, text="g: costo real | h: heurística | f: g+h", font=("Arial", 12, "bold"), bg="#FCF75E").pack(pady=5)

        # Lista de pasos
        self.listbox = tk.Listbox(right_frame, width=50, font=("Courier", 10))
        self.listbox.insert(tk.END, "Paso | Estado             | g | h  | f  ")
        self.listbox.insert(tk.END, "-----+---------------------+---+----+----")
        self.listbox.pack(pady=5, fill="y", expand=True)

        self.btn = tk.Button(root, font="-family {Segoe UI Black} -size 12 -weight bold",
                             background="#FCF75E", text="Siguiente Paso", command=self.siguiente)
        self.btn.pack(pady=5)

        # Guardar camino y mostrar primero
        self.path = path
        self.index = 0
        self.draw_state(self.path[0])
        self.add_to_listbox(self.path[0])

    def draw_state(self, node):
        state = node.state
        self.canvas.delete("all")
        c_izq, m_izq, bote, c_der, m_der = state

        self.canvas.create_text(100, 20, text="Orilla Izquierda", font=("Arial", 14))
        self.canvas.create_text(600, 20, text="Orilla Derecha", font=("Arial", 14))
        self.canvas.create_text(350, 240, text=f"Estado: {state}", font=("Arial", 12))

        self.canvas.create_oval(150, 260, 170, 280, fill="red")
        self.canvas.create_text(190, 270, text="Caníbal", anchor="w", font=("Arial", 10))

        self.canvas.create_oval(300, 260, 320, 280, fill="green")
        self.canvas.create_text(340, 270, text="Misionero", anchor="w", font=("Arial", 10))

        if bote == 0:
            self.canvas.create_rectangle(150, 200, 210, 230, fill="brown", tags="bote")
            self.canvas.create_text(180, 215, text="BOTE", fill="white", font=("Arial", 10))
        else:
            self.canvas.create_rectangle(490, 200, 550, 230, fill="brown", tags="bote")
            self.canvas.create_text(520, 215, text="BOTE", fill="white", font=("Arial", 10))

        for i in range(c_izq):
            self.canvas.create_oval(50 + i*25, 60, 70 + i*25, 80, fill="red")
        for i in range(m_izq):
            self.canvas.create_oval(50 + i*25, 100, 70 + i*25, 120, fill="green")

        for i in range(c_der):
            self.canvas.create_oval(600 + i*25, 60, 620 + i*25, 80, fill="red")
        for i in range(m_der):
            self.canvas.create_oval(600 + i*25, 100, 620 + i*25, 120, fill="green")

    def add_to_listbox(self, node):
        s = node.state
        line = f"Paso {self.index + 1}: {s}   g={node.g} h={node.h:.1f} f={node.f:.1f}"
        self.listbox.insert(tk.END, line)

    def siguiente(self):
        self.index += 1
        if self.index < len(self.path):
            self.draw_state(self.path[self.index])
            self.add_to_listbox(self.path[self.index])
        else:
            self.btn.config(state=tk.DISABLED)
            self.canvas.create_text(600, 280, text="¡Solución completada!", font=("Arial", 14), fill="darkgreen")

if __name__ == "__main__":
    path = astar()
    if path:
        root = tk.Tk()
        app = App(root, path)
        root.mainloop()
    else:
        print("No se encontró solución")
