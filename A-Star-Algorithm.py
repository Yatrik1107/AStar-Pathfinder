import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import heapq
import time

global message 
message = ""

# A* Algorithm Code
class Node:
    def __init__(self, points, parent=None):
        self.points = points
        self.parent = parent
        self.f = 0
        self.g = 0
        self.h = 0

    def __lt__(self, another_node):
        return self.f < another_node.f

def calculate_h_score(source, target):
    return abs(source[0] - target[0]) + abs(source[1] - target[1])

def get_neighbours(grid, node):
    pos = node.points
    neighbours_list = [(pos[0]-1, pos[1]), (pos[0]+1, pos[1]), (pos[0], pos[1]-1), (pos[0], pos[1]+1)]
    valid_neighbours = []
    for i, j in neighbours_list:
        if (0 <= j < len(grid[0])) and (0 <= i < len(grid)) and (grid[i][j] == 0):
            valid_neighbours.append((i, j))
    return valid_neighbours

def add_to_open_set(open_set, node):
    for i in open_set:
        if i.points == node.points and node.g >= i.g:
            return False
    return True

def reconstruct_path(current_node):
    path = []
    while current_node:
        path.append(current_node.points)
        current_node = current_node.parent
    return path[::-1]

def astar(grid, start, goal):
    start_node = Node(start)
    goal_node = Node(goal)
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)
        closed_set.add(current_node.points)
        if current_node.points == goal_node.points:
            return reconstruct_path(current_node)

        neighbours_list = get_neighbours(grid, current_node)
        for i in neighbours_list:
            n_node = Node(i, current_node)
            if n_node.points in closed_set:
                continue

            n_node.g = current_node.g + 1
            n_node.h = calculate_h_score(n_node.points, goal_node.points)
            n_node.f = n_node.g + n_node.h

            if not add_to_open_set(open_set, n_node):
                continue

            heapq.heappush(open_set, n_node)

    return None

grid = [
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
]

start = None
goal = None
path = None  
path_index = 0 

def input_start(start_point):
    global start, message
    try:
        start_point = start_point.replace('(', '').replace(')', '').strip()
        start = tuple(map(int, start_point.split(',')))
        if grid[start[0]][start[1]] == 1:
            message = "Invalid start point. It's an obstacle."
            start = None
        else:
            message = f"Start point set to: {start}"
    except (ValueError, IndexError):
        message = "Invalid start point format or out of bounds."

def input_goal(goal_point):
    global goal, message
    try:
        goal_point = goal_point.replace('(', '').replace(')', '').strip()
        goal = tuple(map(int, goal_point.split(',')))
        if grid[goal[0]][goal[1]] == 1:
            message = "Invalid goal point. It's an obstacle."
            goal = None
        else:
            message = f"Goal point set to: {goal}"
    except (ValueError, IndexError):
        message = "Invalid goal point format or out of bounds."

def find_path():
    global path, path_index, message
    if start is not None and goal is not None:
        path = astar(grid, start, goal)
        if path:
            path_index = 0
            message = "Path found!"
        else:
            message = "No path found."
    else:
        message = "Please set both start and goal points."

def draw(canvas):
    global path_index
    frame_width = 600
    frame_height = 600
    rows = len(grid)
    cols = len(grid[0])
    cell_size = min(frame_width // cols, frame_height // rows) 
    
    for i in range(rows):
        for j in range(cols):
            color = "White"
            if grid[i][j] == 1:
                color = "Black"
            canvas.draw_polygon(
                [(j * cell_size, i * cell_size), (j * cell_size, (i + 1) * cell_size),
                 ((j + 1) * cell_size, (i + 1) * cell_size), ((j + 1) * cell_size, i * cell_size)],
                1, "Grey", color
            )
    
    if start:
        canvas.draw_circle((start[1] * cell_size + cell_size / 2, start[0] * cell_size + cell_size / 2), cell_size // 2.5, 5, "Green")
    
    if goal:
        canvas.draw_circle((goal[1] * cell_size + cell_size / 2, goal[0] * cell_size + cell_size / 2), cell_size // 2.5, 5, "Red")
    
    if path:
        for i in range(min(path_index, len(path) - 1)):
            point_a = path[i]
            point_b = path[i + 1]
            canvas.draw_line(
                (point_a[1] * cell_size + cell_size / 2, point_a[0] * cell_size + cell_size / 2),
                (point_b[1] * cell_size + cell_size / 2, point_b[0] * cell_size + cell_size / 2),
                5, "Yellow"
            )
    
        if path_index < len(path) - 1:
            path_index += 1

    canvas.draw_text(message, (10, 610), 20, "White")

frame = simplegui.create_frame("A* Pathfinding", 585, 620)

frame.set_draw_handler(draw)
frame.add_input("Set Start Point (row, col):", input_start, 200)
frame.add_input("Set Goal Point (row, col):", input_goal, 200)
frame.add_button("Find Path", find_path, 100)

frame.start()
