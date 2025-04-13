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

    def is_goal(self): #Estado Meta
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
            path.append(node.state)
            node = node.parent
        return path[::-1]

def astar():
    start = Node((3, 3, 0, 0, 0)) #Estado inicial
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

#Interface
class App:
    def __init__(self, root, path):
        self.root = root
        self.root.title("A* - Misioneros y Caníbales")
        self.canvas = tk.Canvas(root, width=700, height=300, bg="#F4F1D6")
        self.canvas.pack()
        self.path = path
        self.index = 0

        self.btn = tk.Button(root,font="-family {Segoe UI Black} -size 12 -weight bold",
        background="#FCF75E",text="Siguiente Paso", command=self.siguiente)
        self.btn.pack()

        self.draw_state(self.path[0])

    def draw_state(self, state):
        self.canvas.delete("all")
        c_izq, m_izq, bote, c_der, m_der = state

        # Etiquetas
        self.canvas.create_text(100, 20, text="Orilla Izquierda", font=("Arial", 14))
        self.canvas.create_text(600, 20, text="Orilla Derecha", font=("Arial", 14))
        self.canvas.create_text(350, 240, text=f"Estado: {state}", font=("Arial", 12))

        self.canvas.create_oval(150, 260, 170, 280, fill="red")
        self.canvas.create_text(190, 270, text="Caníbal", anchor="w", font=("Arial", 10))

        self.canvas.create_oval(300, 260, 320, 280, fill="green")
        self.canvas.create_text(340, 270, text="Misionero", anchor="w", font=("Arial", 10))


        # Bote
        if bote == 0:
            self.canvas.create_rectangle(150, 200, 210, 230, fill="brown", tags="bote")
            self.canvas.create_text(180, 215, text="BOTE", fill="white", font=("Arial", 10))
        else:
            self.canvas.create_rectangle(490, 200, 550, 230, fill="brown", tags="bote")
            self.canvas.create_text(520, 215, text="BOTE", fill="white", font=("Arial", 10))

        # Dibujar personajes
        for i in range(c_izq):
            self.canvas.create_oval(50 + i*25, 60, 70 + i*25, 80, fill="red")  # Caníbales izquierda
        for i in range(m_izq):
            self.canvas.create_oval(50 + i*25, 100, 70 + i*25, 120, fill="green")  # Misioneros izquierda

        for i in range(c_der):
            self.canvas.create_oval(600 + i*25, 60, 620 + i*25, 80, fill="red")  # Caníbales derecha
        for i in range(m_der):
            self.canvas.create_oval(600 + i*25, 100, 620 + i*25, 120, fill="green")  # Misioneros derecha

    def siguiente(self):
        self.index += 1
        if self.index < len(self.path):
            self.draw_state(self.path[self.index])
        else:
            self.btn.config(state=tk.DISABLED)
            self.canvas.create_text(350, 280, text="¡Solución completada!", font=("Arial", 14), fill="darkgreen")


if __name__ == "__main__":
    path = astar()
    if path:
        root = tk.Tk()
        app = App(root, path)
        root.mainloop()
    else:
        print("No se encontró solución")
