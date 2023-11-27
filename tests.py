import unittest
from main import Maze, Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 7
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(100, 100))
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )


if __name__ == "__main__":
    unittest.main()
