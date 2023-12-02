from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

WALL_CLR = "#E0E0FF"
BACK_CLR = "#353540"
MOVE_CLR = "green"
UNDO_CLR = "brown"


class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__root = Tk()
        self.__root.title = "The Maize"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas(
            width=self.width, height=self.height, bg=BACK_CLR)
        self.__canvas.pack(fill=BOTH, side='left', expand=1)

        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        x1 = self.p1.x
        y1 = self.p1.y
        x2 = self.p2.x
        y2 = self.p2.y
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=3)
        canvas.pack()


class Cell():
    def __init__(
        self, _x1, _x2, _y1, _y2, _win, has_left_wall=True,
        has_right_wall=True, has_top_wall=True, has_bottom_wall=True
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win
        self.visited = False

    def draw(self):
        top_left = Point(self._x1, self._y1)
        top_right = Point(self._x2, self._y1)
        bottom_left = Point(self._x1, self._y2)
        bottom_right = Point(self._x2, self._y2)

        top_clr = WALL_CLR if self.has_top_wall else BACK_CLR
        bot_clr = WALL_CLR if self.has_bottom_wall else BACK_CLR
        left_clr = WALL_CLR if self.has_left_wall else BACK_CLR
        right_clr = WALL_CLR if self.has_right_wall else BACK_CLR

        self._win.draw_line(Line(top_left, top_right), top_clr)
        self._win.draw_line(Line(top_left, bottom_left), left_clr)
        self._win.draw_line(Line(bottom_left, bottom_right), bot_clr)
        self._win.draw_line(Line(top_right, bottom_right), right_clr)

    def draw_move(self, to_cell, undo=False):
        move_x1 = (self._x1 + self._x2) / 2
        move_y1 = (self._y1 + self._y2) / 2
        move_p1 = Point(move_x1, move_y1)

        move_x2 = (to_cell._x1 + to_cell._x2) / 2
        move_y2 = (to_cell._y1 + to_cell._y2) / 2
        move_p2 = Point(move_x2, move_y2)

        if undo:
            move_color = UNDO_CLR
        else:
            move_color = MOVE_CLR

        self._win.draw_line(Line(move_p1, move_p2), move_color)


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
        seed
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.seed = None

        random.seed(self.seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(2, 2)
        self._reset_cells_visited()
        self.solve()
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for c in range(self.num_cols):
            self._cells.append([])
            x1 = c * self.cell_size_x + self.x1
            x2 = (c+1) * self.cell_size_x + self.x1

            for r in range(self.num_rows):
                y1 = r * self.cell_size_y + self.y1
                y2 = (r+1) * self.cell_size_y + self.y1
                new_cell = Cell(x1, x2, y1, y2, self.win)
                self._cells[c].append(new_cell)

                self._draw_cell(c, r)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        sleep(0.02)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)

        i_last = self.num_cols - 1
        j_last = self.num_rows - 1
        self._cells[i_last][j_last].has_bottom_wall = False
        self._draw_cell(i_last, j_last)

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True

        while True:
            cells_to_check = []

            if i > 0:
                left_cell = self._cells[i-1][j]
                if not left_cell.visited:
                    cells_to_check.append((i-1, j))

            if i < (self.num_cols-1):
                right_cell = self._cells[i+1][j]
                if not right_cell.visited:
                    cells_to_check.append((i+1, j))

            if j > 0:
                above_cell = self._cells[i][j-1]
                if not above_cell.visited:
                    cells_to_check.append((i, j-1))

            if j < (self.num_rows-1):
                below_cell = self._cells[i][j+1]
                if not below_cell.visited:
                    cells_to_check.append((i, j+1))

            if len(cells_to_check) == 0:
                return
            else:
                new_i, new_j = random.choice(cells_to_check)
                if new_i == i-1:
                    self._cells[new_i][new_j].has_right_wall = False
                    self._cells[i][j].has_left_wall = False
                elif new_i == i+1:
                    self._cells[new_i][new_j].has_left_wall = False
                    self._cells[i][j].has_right_wall = False
                elif new_j == j-1:
                    self._cells[new_i][new_j].has_bottom_wall = False
                    self._cells[i][j].has_top_wall = False
                elif new_j == j+1:
                    self._cells[new_i][new_j].has_top_wall = False
                    self._cells[i][j].has_bottom_wall = False

                self._draw_cell(new_i, new_j)
                self._break_walls_r(new_i, new_j)

    def _reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True

        if i == self.num_cols-1 and j == self.num_rows-1:
            return True

        if i > 0:
            left_cell = self._cells[i-1][j]
            if not left_cell.has_right_wall and not left_cell.visited:
                cell.draw_move(left_cell)
                if self._solve_r(i-1, j):
                    return True
                else:
                    cell.draw_move(left_cell, undo=True)

        if i < (self.num_cols-1):
            right_cell = self._cells[i+1][j]
            if not right_cell.has_left_wall and not right_cell.visited:
                cell.draw_move(right_cell)
                if self._solve_r(i+1, j):
                    return True
                else:
                    cell.draw_move(right_cell, undo=True)

        if j > 0:
            above_cell = self._cells[i][j-1]
            if not above_cell.has_bottom_wall and not above_cell.visited:
                cell.draw_move(above_cell)
                if self._solve_r(i, j-1):
                    return True
                else:
                    cell.draw_move(above_cell, undo=True)

        if j < (self.num_rows-1):
            below_cell = self._cells[i][j+1]
            if not below_cell.has_top_wall and not below_cell.visited:
                cell.draw_move(below_cell)
                if self._solve_r(i, j+1):
                    return True
                else:
                    cell.draw_move(below_cell, undo=True)

        return False


if __name__ == "__main__":
    win = Window(820, 820)

    # test_cell_1 = Cell(50, 100, 50, 100, win, has_top_wall=False)
    # test_cell_2 = Cell(100, 150, 50, 100, win, has_bottom_wall=False)
    # test_cell_1.draw()
    # test_cell_2.draw()
    # test_cell_1.draw_move(test_cell_2, undo=True)

    test_maze = Maze(10, 10, 10, 10, 80, 80, win, seed=42)
    win.wait_for_close()
