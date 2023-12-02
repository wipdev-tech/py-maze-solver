import unittest
from main import Maze, Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 5
        num_rows = 5
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(100, 100), seed=10)
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
        num_cols = 4
        num_rows = 6
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(100, 100), seed=10)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[3][5].has_bottom_wall)

    def test_walls_unvisited(self):
        num_cols = 6
        num_rows = 7
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(100, 100), seed=10)
        for i in range(m1.num_cols):
            for j in range(m1.num_rows):
                self.assertFalse(m1._cells[i][j].visited)
                self.assertFalse(m1._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()
