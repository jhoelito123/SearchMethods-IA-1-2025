import heapq

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
            path_goal = current_goal.get_path()
            path_start = parents_start[current_goal.state].get_path()[::-1]
            return path_start + path_goal[1:]
        visited_goal.add(current_goal.state)
        
        for child in current_goal.get_children():
            if child.state not in visited_goal:
                parents_goal[child.state] = current_goal
                heapq.heappush(open_set_goal, child)
    
    return None
