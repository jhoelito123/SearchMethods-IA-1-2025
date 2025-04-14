import tkinter as tk
from tkinter import messagebox, Toplevel, Label
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import copy


def board_to_str(board):
    return "\n" + "\n-----------\n".join([" | ".join(cell or " " for cell in row) for row in board])


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


ab_trace = []
node_counter = 0
search_tree = nx.DiGraph()
node_labels = {}


def alphabeta_traced_tree(board, depth, alpha, beta, is_maximizing, parent=None):
    global ab_trace, node_counter, search_tree, node_labels
    node_id = node_counter
    node_counter += 1
    tablero = board_to_str(board)
    if parent is not None:
        search_tree.add_edge(parent, node_id)

    if is_winner(board, 'O'):
        node_labels[node_id] = f"D{depth}\nO gana\n+1\n{tablero}"
        ab_trace.append((depth, 'O WIN', alpha, beta, 1))
        return 1, None
    elif is_winner(board, 'X'):
        node_labels[node_id] = f"D{depth}\nX gana\n-1\n{tablero}"
        ab_trace.append((depth, 'X WIN', alpha, beta, -1))
        return -1, None
    elif is_draw(board):
        node_labels[node_id] = f"D{depth}\nEmpate\n0\n{tablero}"
        ab_trace.append((depth, 'DRAW', alpha, beta, 0))
        return 0, None

    best_move = None
    if is_maximizing:
        max_eval = -float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = 'O'
            eval, _ = alphabeta_traced_tree(
                board, depth + 1, alpha, beta, False, node_id)
            board[i][j] = ''
            ab_trace.append((depth, f'MAX {i},{j}', alpha, beta, eval))
            if eval > max_eval:
                max_eval = eval
                best_move = (i, j)
            alpha = max(alpha, eval)
            if beta <= alpha:
                node_labels[node_id] = f"D{depth}\nPODA\nα={alpha:.1f} β={beta:.1f}\n{tablero}"
                ab_trace.append(
                    (depth, f'PODA MAX en {i},{j}', alpha, beta, max_eval))
                return max_eval, best_move
        node_labels[node_id] = f"D{depth}\nMAX\n{max_eval}\n{tablero}"
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for i, j in get_available_moves(board):
            board[i][j] = 'X'
            eval, _ = alphabeta_traced_tree(
                board, depth + 1, alpha, beta, True, node_id)
            board[i][j] = ''
            ab_trace.append((depth, f'MIN {i},{j}', alpha, beta, eval))
            if eval < min_eval:
                min_eval = eval
                best_move = (i, j)
            beta = min(beta, eval)
            if beta <= alpha:
                node_labels[node_id] = f"D{depth}\nPODA\nα={alpha:.1f} β={beta:.1f}\n{tablero}"
                ab_trace.append(
                    (depth, f'PODA MIN en {i},{j}', alpha, beta, min_eval))
                return min_eval, best_move
        node_labels[node_id] = f"D{depth}\nMIN\n{min_eval}\n{tablero}"
        return min_eval, best_move


def hierarchy_pos(G, root=None, vert_gap=0.3, vert_loc=0, xcenter=0.5):
    pos = {}
    levels = {}

    def assign_levels(node, depth):
        levels.setdefault(depth, []).append(node)
        for child in G.successors(node):
            assign_levels(child, depth + 1)
    if root is None:
        root = list(nx.topological_sort(G))[0]
    assign_levels(root, 0)
    max_width = max(len(nodes) for nodes in levels.values())
    width = max_width * 1.0

    def _hierarchy_pos(G, node, left, right, vert_loc, depth):
        pos[node] = ((left + right) / 2, vert_loc)
        children = list(G.successors(node))
        if children:
            dx = (right - left) / len(children)
            nextx = left
            for child in children:
                _hierarchy_pos(G, child, nextx, nextx + dx,
                               vert_loc - vert_gap, depth + 1)
                nextx += dx
    _hierarchy_pos(G, root, 0, width, vert_loc, 0)
    return pos


class TicTacToeAlphaBeta:
    def __init__(self, root):
        self.root = root
        self.root.title("Tres en Raya - IA con Poda Alpha-Beta")
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.fig = None
        self.ax = None
        self.tree_window = None
        self.fig_canvas = None
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text='', font=('Arial', 36), width=5, height=2,
                                command=lambda r=i, c=j: self.human_move(r, c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        tk.Button(self.root, text="Reiniciar", font=('Arial', 14),
                  command=self.reset_board).grid(row=3, column=0, sticky="nsew")
        tk.Button(self.root, text="Ver Proceso IA", font=('Arial', 14),
                  command=self.mostrar_proceso_alpha_beta).grid(row=3, column=1, sticky="nsew")
        tk.Button(self.root, text="Ver Árbol IA", font=('Arial', 14),
                  command=self.abrir_ventana_arbol).grid(row=3, column=2, sticky="nsew")
        tk.Button(self.root, text="Salir", font=('Arial', 14),
                  command=self.root.quit).grid(row=4, column=0, columnspan=3, sticky="nsew")

    def human_move(self, i, j):
        if self.board[i][j] == '':
            self.board[i][j] = 'X'
            self.buttons[i][j].config(text='X', state='disabled')
            if self.check_end('X'):
                return
            self.root.after(300, self.ai_move)

    def ai_move(self):
        global ab_trace, node_counter, search_tree, node_labels
        ab_trace = []
        node_counter = 0
        search_tree.clear()
        node_labels.clear()

        _, move = alphabeta_traced_tree(copy.deepcopy(
            self.board), 0, -float('inf'), float('inf'), True)

        if move:
            i, j = move
            self.board[i][j] = 'O'
            self.buttons[i][j].config(text='O', state='disabled')
            self.check_end('O')
            self.actualizar_arbol()

    def check_end(self, player):
        if is_winner(self.board, player):
            messagebox.showinfo(
                "Fin del juego", f"{'¡Ganaste!' if player == 'X' else 'La IA ganó'}")
            self.disable_buttons()
            return True
        elif is_draw(self.board):
            messagebox.showinfo("Fin del juego", "Empate")
            return True
        return False

    def disable_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')

    def reset_board(self):
        global ab_trace, node_counter, search_tree, node_labels
        ab_trace = []
        node_counter = 0
        search_tree.clear()
        node_labels.clear()
        self.board = [['' for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text='', state='normal')
        self.actualizar_arbol()

    def mostrar_proceso_alpha_beta(self):
        ventana = Toplevel()
        ventana.title("Proceso Alpha-Beta")
        for depth, label, alpha, beta, value in ab_trace:
            texto = f"{'  ' * depth}Nivel {depth} | {label} | α={alpha:.1f}, β={beta:.1f} → valor={value}"
            Label(ventana, text=texto, font=("Courier", 10),
                  anchor="w", justify="left").pack(anchor="w", padx=10)

    def abrir_ventana_arbol(self):
        self.tree_window = Toplevel(self.root)
        self.tree_window.title("Árbol Alpha-Beta")
        self.fig, self.ax = plt.subplots(figsize=(28, 14))
        self.fig_canvas = FigureCanvasTkAgg(self.fig, master=self.tree_window)
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.actualizar_arbol()

    def actualizar_arbol(self):
        if self.fig is None or self.ax is None:
            return
        self.ax.clear()
        if len(search_tree.nodes) == 0:
            self.ax.text(0.5, 0.5, "Árbol vacío", ha='center',
                         va='center', fontsize=14)
        else:
            pos = hierarchy_pos(search_tree)
            nx.draw(search_tree, pos, ax=self.ax, with_labels=False,
                    node_size=1800, node_color='lightblue', node_shape='s')
            nx.draw_networkx_labels(
                search_tree, pos, labels=node_labels, ax=self.ax, font_size=6)
        self.ax.set_title("Árbol de Búsqueda - Alpha-Beta")
        self.ax.axis('off')
        self.fig_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeAlphaBeta(root)
    root.mainloop()
