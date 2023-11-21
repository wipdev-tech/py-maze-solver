from tkinter import Tk, Canvas


class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.__root = Tk()
        self.__root.title = "The Maize"
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

        self.__canvas = Canvas()
        self.__canvas.pack()

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
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)
        canvas.pack()


class Cell():
    def __init__(
        self, _x1, _x2, _y1, _y2, _win, has_left_wall=True,
        has_right_wall=True, has_top_wall=True,  has_bottom_wall=True
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

    def draw(self):
        top_l = Point(self._x1, self._y1)
        top_r = Point(self._x2, self._y1)
        bot_l = Point(self._x1, self._y2)
        bot_r = Point(self._x2, self._y2)

        if self.has_left_wall:
            self._win.draw_line(Line(top_l, bot_l), "black")

        if self.has_right_wall:
            self._win.draw_line(Line(top_r, bot_r), "black")

        if self.has_top_wall:
            self._win.draw_line(Line(top_l, top_r), "black")

        if self.has_bottom_wall:
            self._win.draw_line(Line(bot_l, bot_r), "black")

    def draw_move(self, to_cell, undo=False):
        move_x1 = (self._x1 + self._x2) / 2
        move_y1 = (self._y1 + self._y2) / 2
        move_p1 = Point(move_x1, move_y1)

        move_x2 = (to_cell._x1 + to_cell._x2) / 2
        move_y2 = (to_cell._y1 + to_cell._y2) / 2
        move_p2 = Point(move_x2, move_y2)

        if undo:
            move_color = "gray"
        else:
            move_color = "red"

        self._win.draw_line(Line(move_p1, move_p2), move_color)


if __name__ == "__main__":
    win = Window(800, 600)

    test_cell_1 = Cell(50, 100, 50, 100, win, has_top_wall=False)
    test_cell_2 = Cell(100, 150, 50, 100, win, has_bottom_wall=False)
    test_cell_1.draw()
    test_cell_2.draw()

    test_cell_1.draw_move(test_cell_2, True)

    win.wait_for_close()
