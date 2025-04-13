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
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
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

def bidirectional_search():
    start = Node((3, 3, 0, 0, 0))  # Estado inicial
    goal = Node((0, 0, 1, 3, 3))  # Estado meta
    
    open_set_start = []
    open_set_goal = []
    heapq.heappush(open_set_start, start)
    heapq.heappush(open_set_goal, goal)
    
    visited_start = set()
    visited_goal = set()
    
    parents_start = {start.state: None}
    parents_goal = {goal.state: None}
    
    while open_set_start and open_set_goal:
        # Búsqueda desde el estado inicial
        current_start = heapq.heappop(open_set_start)
        if current_start.state in visited_goal:
            # Ruta encontrada, combinar las soluciones
            print(f"¡Búsquedas se cruzaron! Nodo común: {current_start.state}")
            path_start = current_start.get_path()
            path_goal = parents_goal[current_start.state].get_path()[::-1]
            return path_start + path_goal[1:]
        visited_start.add(current_start.state)
        
        for child in current_start.get_children():
            if child.state not in visited_start:
                parents_start[child.state] = current_start
                heapq.heappush(open_set_start, child)
        
        # Búsqueda desde el estado meta
        current_goal = heapq.heappop(open_set_goal)
        if current_goal.state in visited_start:
            # Ruta encontrada, combinar las soluciones
            print(f"¡Búsquedas se cruzaron! Nodo común: {current_start.state}")
            path_goal = current_goal.get_path()
            path_start = parents_start[current_goal.state].get_path()[::-1]
            return path_start + path_goal[1:]
        visited_goal.add(current_goal.state)
        
        for child in current_goal.get_children():
            if child.state not in visited_goal:
                parents_goal[child.state] = current_goal
                heapq.heappush(open_set_goal, child)
    
    return None

class App:
    def __init__(self, root, path):
        self.root = root
        self.root.title("Bidireccional - Misioneros y Caníbales")
        self.canvas = tk.Canvas(root, width=700, height=300, bg="#F4F1D6")
        self.canvas.pack()
        self.path = path
        self.index = 0

        self.btn = tk.Button(root, font="-family {Segoe UI Black} -size 12 -weight bold",
                             background="#FCF75E", text="Siguiente Paso", command=self.siguiente)
        self.btn.pack()

        self.draw_state(self.path[0])

    def draw_state(self, state):
        self.canvas.delete("all")
        c_izq, m_izq, bote, c_der, m_der = state

        # Etiquetas
        self.canvas.create_text(100, 20, text="Orilla Izquierda", font=("Arial", 14))
        self.canvas.create_text(600, 20, text="Orilla Derecha", font=("Arial", 14))
        self.canvas.create_text(350, 240, text=f"Estado: {state}", font=("Arial", 12))

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
    path = bidirectional_search()
    if path:
        root = tk.Tk()
        app = App(root, path)
        root.mainloop()
    else:
        print("No se encontró solución")
