import unittest

from block import Block, Orientation


class BlockMovementTests(unittest.TestCase):
    def test_standing_transitions(self):
        expected = {
            "UP": (Orientation.VERTICAL, (1, 3), (2, 3)),
            "DOWN": (Orientation.VERTICAL, (4, 3), (5, 3)),
            "LEFT": (Orientation.HORIZONTAL, (3, 1), (3, 2)),
            "RIGHT": (Orientation.HORIZONTAL, (3, 4), (3, 5)),
        }
        for action, result in expected.items():
            with self.subTest(action=action):
                block = Block(3, 3)
                block.move(action)
                self.assertEqual((block.orientation, block.pos1, block.pos2), result)

    def test_horizontal_transitions(self):
        horizontal = Block(3, 3)
        horizontal.move("RIGHT")
        expected = {
            "UP": (Orientation.HORIZONTAL, (2, 4), (2, 5)),
            "DOWN": (Orientation.HORIZONTAL, (4, 4), (4, 5)),
            "LEFT": (Orientation.STANDING, (3, 3), (3, 3)),
            "RIGHT": (Orientation.STANDING, (3, 6), (3, 6)),
        }
        for action, result in expected.items():
            with self.subTest(action=action):
                block = horizontal.copy()
                block.move(action)
                self.assertEqual((block.orientation, block.pos1, block.pos2), result)

    def test_vertical_transitions(self):
        vertical = Block(3, 3)
        vertical.move("DOWN")
        expected = {
            "UP": (Orientation.STANDING, (3, 3), (3, 3)),
            "DOWN": (Orientation.STANDING, (6, 3), (6, 3)),
            "LEFT": (Orientation.VERTICAL, (4, 2), (5, 2)),
            "RIGHT": (Orientation.VERTICAL, (4, 4), (5, 4)),
        }
        for action, result in expected.items():
            with self.subTest(action=action):
                block = vertical.copy()
                block.move(action)
                self.assertEqual((block.orientation, block.pos1, block.pos2), result)

    def test_split_cube_switches_and_rejoins(self):
        block = Block.split((1, 1), (1, 4))
        block.move("RIGHT")
        self.assertEqual(block.get_cells(), [(1, 2), (1, 4)])
        block.move("SWITCH")
        self.assertEqual(block.active_index, 1)
        block.move("LEFT")
        self.assertEqual(block.orientation, Orientation.HORIZONTAL)
        self.assertEqual(block.get_cells(), [(1, 2), (1, 3)])


if __name__ == "__main__":
    unittest.main()
