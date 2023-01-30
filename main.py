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




        
def main():
    win = Window(800, 600)
    win.wait_for_close()


if __name__ == "__main__":
    main()