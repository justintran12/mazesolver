from tkinter import Tk, BOTH, Canvas
import time
import random

# Initialize a window GUI with given width and height
class Window:
    def __init__(self, width, height):
        self.window = Tk()
        self.canvas = Canvas(self.window, bg="white", height=height, width=width)
        self.running = False
        # connected to close function, will stop program from running after window is closed
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.title("Maze Solver")
        self.canvas.pack()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)

    # redraw all graphics in window
    def redraw(self):
        self.window.update_idletasks()
        self.window.update()
    
    # continuosly refresh window until closed
    def wait_for_close(self):
        self.running = True
        while (self.running == True):
            self.redraw()

    def close(self):
        self.running = False

# x=0 is left of screen, y=0 is top of screen
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )
        canvas.pack()

# x1, y1 is top left corner of cell and x2,y2 is bottom right corner of cell
class Cell:
    def __init__(self, window = None, x1 = 0, y1 = 0, x2 = 0, y2 = 0, has_left_wall = True, has_right_wall = True, has_top_wall = True, has_bottom_wall = True):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.window = window
        self.visited = False

    def draw(self):
        left_wall = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
        top_wall = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
        right_wall = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
        bottom_wall = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))

        # white matches background, so it visually breaks a wall or doesn't draw it
        if (self.has_left_wall == True):
            self.window.draw_line(left_wall, "black")
        else:
            self.window.draw_line(left_wall, "white")

        if (self.has_top_wall == True):
            self.window.draw_line(top_wall, "black")
        else:
            self.window.draw_line(top_wall, "white")

        if (self.has_right_wall == True):
            self.window.draw_line(right_wall, "black")
        else:
            self.window.draw_line(right_wall, "white")

        if (self.has_bottom_wall == True):
            self.window.draw_line(bottom_wall, "black")
        else:
            self.window.draw_line(bottom_wall, "white")

    # draw line from midpoint of this cell to midpoint of another cell (gray if backtracking)
    def draw_move(self, to_cell, undo=False):
        if (undo == True):
            color = "gray"
        else:
            color = "red"

        self_mid = Point((self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2)
        to_cell_mid = Point((to_cell.x1 + to_cell.x2) / 2, (to_cell.y1 + to_cell.y2) / 2)
        self.window.draw_line(Line(self_mid, to_cell_mid), color)

# x1, y1 are the coordinates for the top left corner of the maze (x1 is pixels from the left of screen, y1 is pixels from the top of screen)
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        if (seed != None):
            random.seed(seed)
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.create_cells()
        #after cells initialized, draw them
        for i in range(num_cols):
            for j in range(num_rows):
                self.draw_cell(i, j)

    # initialize matrix of cells
    def create_cells(self):
        for i in range(self.num_cols):
            col = []
            for j in range(self.num_rows):
                col.append(Cell(self.win))
            self.cells.append(col)

    def draw_cell(self, i, j):
        cell = self.cells[i][j]
        cell.x1 = self.x1 + (i * self.cell_size_x)
        cell.y1 = self.y1 + (j * self.cell_size_y)
        cell.x2 = cell.x1 + self.cell_size_x
        cell.y2 = cell.y1 + self.cell_size_y
        cell.draw()
        self.animate()

    # entrance to maze is top of top-left cell, exit is bottom of bottom right cell
    def break_entrance_and_exit(self):
        top_left_cell = self.cells[0][0]
        bottom_right_cell = self.cells[self.num_cols - 1][self.num_rows - 1]

        top_left_cell.has_top_wall = False
        bottom_right_cell.has_bottom_wall = False
        self.draw_cell(0,0)
        self.draw_cell(self.num_cols - 1, self.num_rows - 1)

    # i, j passed in is coords of current cell in matrix (0,0 is top left corner)
    def break_walls_r(self, i, j) :
        neighbors = []
        neighbors = self.get_neighbors(i, j)
        self.cells[i][j].visited = True
        while (len(neighbors) > 0):
            # choose random neighbor to go to
            rand_ind = random.randrange(len(neighbors))
            chosen_coords = neighbors.pop(rand_ind)
            chosen_cell = self.cells[chosen_coords[0]][chosen_coords[1]]
            if (chosen_cell.visited == False):
                # knock down walls between current cell and chosen neighbor cell
                self.knock_down(i, j, chosen_coords[0], chosen_coords[1])
                # move to chosen cell
                self.break_walls_r(chosen_coords[0], chosen_coords[1])
        # if current cell has no neighbors available to go to or is done going through its neighbors, draw current cell
        self.draw_cell(i, j)

    def solve(self):
        return self.solve_r(0, 0)
    
    # solve the maze use recursive DFS backtracking algorithm
    def solve_r(self, i, j):
        self.animate()
        curr_cell = self.cells[i][j]
        curr_cell.visited = True
        # if curr cell is the end cell return true
        if (i == self.num_cols - 1 and j == self.num_rows - 1):
            return True

        neighbors = self.get_neighbors(i, j)
        while (len(neighbors) > 0):
            neighbor_ind = neighbors.pop(0)
            neighbor_cell = self.cells[neighbor_ind[0]][neighbor_ind[1]]
            # if chosen neighbor cell is not already visited and a wall does not exist between the curr and chosen cell
            # then draw red line between curr and chosen cell and move onto that chosen cell
            if (neighbor_cell.visited == False and self.wall_exists(i, j, neighbor_ind[0], neighbor_ind[1])== False):
                curr_cell.draw_move(neighbor_cell)
                # if path gives us correct solution return true otherwise backtrack by drawing gray line
                if (self.solve_r(neighbor_ind[0], neighbor_ind[1]) == True):
                    return True
                else:
                    curr_cell.draw_move(neighbor_cell, undo = True)
        return False

    # check if wall exists between curr cell and chosen cell
    def wall_exists(self, curr_i, curr_j, chosen_i, chosen_j):
        chosen_cell = self.cells[chosen_i][chosen_j]
        if (curr_i != chosen_i):
            if (curr_i < chosen_i):
                # right neighbor is chosen
                return chosen_cell.has_left_wall
            else:
                # left neighbor chosen
                return chosen_cell.has_right_wall
        else:
            if (curr_j < chosen_j):
                # bottom neighbor chosen
                return chosen_cell.has_top_wall
            else:
                # top neighbor chosen
                return chosen_cell.has_bottom_wall

    # get valid adjacent neighbors from curr cell
    def get_neighbors(self, i, j):
        neighbors = []
        if (j > 0):
            top_neighbor = [i, j - 1]
            if (self.cells[top_neighbor[0]][top_neighbor[1]].visited == False):
                neighbors.append(top_neighbor)
        if (i < self.num_cols - 1):
            right_neighbor = [i + 1, j]
            if (self.cells[right_neighbor[0]][right_neighbor[1]].visited == False):
                neighbors.append(right_neighbor)
        if (j < self.num_rows - 1):
            bot_neighbor = [i, j + 1]
            if (self.cells[bot_neighbor[0]][bot_neighbor[1]].visited == False):
                neighbors.append(bot_neighbor)       
        if (i > 0):
            left_neighbor = [i - 1, j]
            if (self.cells[left_neighbor[0]][left_neighbor[1]].visited == False):
                neighbors.append(left_neighbor)    
        return neighbors   

    # knock down wall between curr cell and chosen cell
    def knock_down(self, curr_i, curr_j, chosen_i, chosen_j):
        curr_cell = self.cells[curr_i][curr_j]
        chosen_cell = self.cells[chosen_i][chosen_j]
        # top neighbor chosen
        if (curr_j - 1 == chosen_j):
            curr_cell.has_top_wall = False
            chosen_cell.has_bottom_wall = False
        elif (curr_j + 1 == chosen_j): # bot neighbor chosen
            curr_cell.has_bottom_wall = False
            chosen_cell.has_top_wall = False
        elif (curr_i - 1 == chosen_i): # left neighbor chosen
            curr_cell.has_left_wall = False
            chosen_cell.has_right_wall = False
        else: # right neighbor chosen
            curr_cell.has_right_wall = False
            chosen_cell.has_left_wall = False

    # reset visited field after carving maze
    def reset_cells_visited(self):
        for col in self.cells:
            for cell in col:
                cell.visited = False

    # delay and redraw to allow visualization of graphics
    def animate(self):
        self.win.redraw()
        time.sleep(0.05)

