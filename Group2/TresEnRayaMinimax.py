import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import copy


def board_to_str(board):
    lines = []
    for row in board:
        lines.append(" | ".join(cell or " " for cell in row))
    return "\n" + "\n-----------\n".join(lines)


def is_winner(board, player):
    win_states = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_states


def is_draw(board):
    return all(cell != '' for row in board for cell in row)


def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']


def evaluate_heuristic(board):
    lines = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]

    def count_opportunities(player):
        return sum(all(c == player or c == '' for c in line) and any(c == '' for c in line) for line in lines)

    return count_opportunities('X') - count_opportunities('O')


minimax_tree = nx.DiGraph()
minimax_labels = {}
node_id_counter = 0
node_depths = {}


def minimax_with_tree(board, is_maximizing, parent=None, depth=0, max_depth=4):
    global node_id_counter, minimax_tree, minimax_labels, node_depths
    current_id = node_id_counter
    node_id_counter += 1
    node_depths[current_id] = depth

    if parent is not None:
        minimax_tree.add_edge(parent, current_id)

    if is_winner(board, 'O'):
        minimax_labels[current_id] = f"MAX\n{board_to_str(board)}\n→ +1"
        return 1, None
    elif is_winner(board, 'X'):
        minimax_labels[current_id] = f"MIN\n{board_to_str(board)}\n→ -1"
        return -1, None
    elif is_draw(board):
        minimax_labels[current_id] = f"EMPATE\n{board_to_str(board)}\n→ 0"
        return 0, None
    elif depth >= max_depth:
        heuristic = evaluate_heuristic(board)
        minimax_labels[current_id] = f"H{depth}\n{board_to_str(board)}\n→ {heuristic}"
        return heuristic, None

    best_move = None
    if is_maximizing:
        best_score = -float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = 'O'
            score, _ = minimax_with_tree(
                board, False, current_id, depth + 1, max_depth)
            board[i][j] = ''
            if score > best_score:
                best_score = score
                best_move = (i, j)
        minimax_labels[current_id] = f"MAX\n{board_to_str(board)}\n→ {best_score}"
        return best_score, best_move
    else:
        best_score = float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = 'X'
            score, _ = minimax_with_tree(
                board, True, current_id, depth + 1, max_depth)
            board[i][j] = ''
            if score < best_score:
                best_score = score
                best_move = (i, j)
        minimax_labels[current_id] = f"MIN\n{board_to_str(board)}\n→ {best_score}"
        return best_score, best_move


def hierarchy_pos(G, root=None, width=1., vert_gap=0.3, vert_loc=0, xcenter=0.5, max_depth=3):
    pos = {}

    def _hierarchy_pos(G, root, left, right, vert_loc, depth):
        if depth > max_depth:
            return
        pos[root] = ((left + right) / 2, vert_loc)
        neighbors = list(G.successors(root))
        if neighbors:
            dx = (right - left) / len(neighbors)
            nextx = left
            for neighbor in neighbors:
                _hierarchy_pos(G, neighbor, nextx, nextx + dx,
                               vert_loc - vert_gap, depth + 1)
                nextx += dx

    if root is None:
        try:
            root = list(nx.topological_sort(G))[0]
        except IndexError:
            return pos
    _hierarchy_pos(G, root, 0, width, vert_loc, 0)
    return pos


class MinimaxTreeViewer:
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Árbol Minimax")
        self.fig, self.ax = plt.subplots(figsize=(14, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def actualizar_arbol(self):
        self.ax.clear()
        if len(minimax_tree) == 0:
            self.ax.text(0.5, 0.5, "Árbol vacío", ha='center',
                         va='center', fontsize=14)
        else:
            visible_nodes = {n for n, d in node_depths.items() if d <= 3}
            visible_tree = minimax_tree.subgraph(visible_nodes).copy()
            visible_labels = {n: minimax_labels[n] for n in visible_tree.nodes}
            try:
                root = list(nx.topological_sort(visible_tree))[0]
                pos = hierarchy_pos(visible_tree, root=root, max_depth=3)
                nx.draw(visible_tree, pos, ax=self.ax, with_labels=False,
                        node_size=1800, node_color='lightblue', node_shape='s')
                nx.draw_networkx_labels(
                    visible_tree, pos, labels=visible_labels, font_size=6, ax=self.ax)
            except Exception as e:
                self.ax.text(
                    0.5, 0.5, f"Error: {str(e)}", ha='center', va='center')

        self.ax.set_title(
            "Árbol de Búsqueda - Minimax (máx. 3 niveles visibles)")
        self.ax.axis('off')
        self.canvas.draw()


def mostrar_nodos_heuristicos(root):
    ventana = tk.Toplevel(root)
    ventana.title("Nodos evaluados con heurística")
    text = tk.Text(ventana, wrap="none", font=("Courier", 10))
    text.pack(expand=True, fill="both")

    for node, label in minimax_labels.items():
        if label.startswith("H"):  # Nodo heurístico
            profundidad = node_depths.get(node, "?")
            text.insert(
                tk.END, f"Nodo ID: {node} | Profundidad: {profundidad}\n")
            text.insert(tk.END, f"{label}\n")
            text.insert(tk.END, "-"*50 + "\n")


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tres en Raya - Humano vs IA (Minimax con heurística)")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.tree_viewer = None
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', font=('Arial', 36), width=5, height=2,
                                command=lambda row=i, col=j: self.human_move(row, col))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        tk.Button(self.root, text="Reiniciar", font=('Arial', 14),
                  command=self.reset_board).grid(row=3, column=0, sticky="nsew")
        tk.Button(self.root, text="Ver Árbol IA", font=('Arial', 14),
                  command=self.show_tree).grid(row=3, column=1, sticky="nsew")
        tk.Button(self.root, text="Salir", font=('Arial', 14),
                  command=self.root.quit).grid(row=4, column=0, columnspan=3, sticky="nsew")

        # ✅ NUEVO BOTÓN
        tk.Button(self.root, text="Ver Heurísticas", font=('Arial', 14),
                  command=lambda: mostrar_nodos_heuristicos(self.root)).grid(row=3, column=2, sticky="nsew")

    def human_move(self, i, j):
        if self.board[i][j] == '':
            self.board[i][j] = 'X'
            self.buttons[i][j].config(text='X', state='disabled')
            if is_winner(self.board, 'X'):
                messagebox.showinfo("Fin del juego", "¡Ganaste!")
                self.disable_all_buttons()
                return
            elif is_draw(self.board):
                messagebox.showinfo("Fin del juego", "Empate")
                return
            self.root.after(500, self.ai_move)

    def ai_move(self):
        global node_id_counter, minimax_tree, minimax_labels, node_depths
        node_id_counter = 0
        minimax_tree.clear()
        minimax_labels.clear()
        node_depths.clear()

        _, move = minimax_with_tree(copy.deepcopy(self.board), True)

        if move:
            i, j = move
            self.board[i][j] = 'O'
            self.buttons[i][j].config(text='O', state='disabled')
            if is_winner(self.board, 'O'):
                messagebox.showinfo("Fin del juego", "La IA ganó")
                self.disable_all_buttons()
            elif is_draw(self.board):
                messagebox.showinfo("Fin del juego", "Empate")

        if self.tree_viewer:
            self.tree_viewer.actualizar_arbol()

    def show_tree(self):
        if self.tree_viewer is None or not self.tree_viewer.window.winfo_exists():
            self.tree_viewer = MinimaxTreeViewer(self.root)
        self.tree_viewer.actualizar_arbol()

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')

    def reset_board(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
        global node_id_counter, minimax_tree, minimax_labels, node_depths
        node_id_counter = 0
        minimax_tree.clear()
        minimax_labels.clear()
        node_depths.clear()
        if self.tree_viewer:
            self.tree_viewer.actualizar_arbol()


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
