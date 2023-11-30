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
        self.assertEqual(
            m1._cells[1][1]._x1,
            10,
        )
        self.assertEqual(
            m1._cells[1][1]._y1,
            10,
        )

    def test_first_last_walls_broken(self):
        num_cols = 7
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(100, 100))
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[6][9].has_bottom_wall)


if __name__ == "__main__":
    unittest.main()
