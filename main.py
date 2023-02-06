from tkinter import Tk, BOTH, Canvas
from maze import Maze
from maze import Window, Cell, Line, Point


def main():
    # test code
    win = Window(800, 600)
    num_rows = 10
    num_cols = 10
    m1 = Maze(50, 50, num_rows, num_cols, 50, 50, win)
    m1.break_entrance_and_exit()
    m1.break_walls_r(0, 0)
    m1.reset_cells_visited()
    if (m1.solve() == True):
        print("Solution found!")
    else: 
        print("No soultion found.")
    win.wait_for_close()


if __name__ == "__main__":
    main()