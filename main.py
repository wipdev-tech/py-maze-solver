from tkinter import Tk, BOTH, Canvas


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


BOTH


if __name__ == "__main__":
    win = Window(800, 600)
    win.wait_for_close()
