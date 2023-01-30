from tkinter import Tk, BOTH, Canvas

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


class Cell:
    def __init__(self, x1, y1, x2, y2, has_left_wall, has_right_wall, has_top_wall, has_bottom_wall, window):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.window = window

    def draw(self):
        if (self.has_left_wall == True):
            print("drawing left wall")
            left_wall = Line(Point(self.x1, self.y1), Point(self.x1, self.y2))
            self.window.draw_line(left_wall, "black")
        if (self.has_top_wall == True):
            top_wall = Line(Point(self.x1, self.y1), Point(self.x2, self.y1))
            self.window.draw_line(left_wall, "black")
        if (self.has_right_wall == True):
            right_wall = Line(Point(self.x2, self.y1), Point(self.x2, self.y2))
            self.window.draw_line(left_wall, "black")
        if (self.has_bottom_wall == True):
            bottom_wall = Line(Point(self.x1, self.y2), Point(self.x2, self.y2))
            self.window.draw_line(left_wall, "black")






        
def main():
    win = Window(800, 600)
    test_cell = Cell(0,0,100,100,True, True, True, True, win)
    test_cell.draw()
    win.wait_for_close()


if __name__ == "__main__":
    main()