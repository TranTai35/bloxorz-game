import json
import tempfile
import unittest
from pathlib import Path

from block import Block, Orientation
from board import Board


class TemporaryBoardTestCase(unittest.TestCase):
    def make_board(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "level.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return Board(path)


class BoardAdvancedTileTests(TemporaryBoardTestCase):
    def test_half_outside_board_is_invalid_without_index_error(self):
        board = self.make_board(
            {
                "grid": ["...", "...", "..."],
                "start": [1, 1],
                "goal": [2, 2],
            }
        )
        result = board.transition(Block(1, 1), board.initial_bridge_states, "UP")
        self.assertFalse(result.valid)
        self.assertEqual(result.block.get_cells(), [(-1, 1), (0, 1)])
        self.assertFalse(board.is_floor(-1, 1, result.bridge_states))
        self.assertTrue(board.is_floor(0, 1, result.bridge_states))

    def test_fragile_tile_rejects_standing_but_supports_lying(self):
        board = self.make_board(
            {
                "grid": [".....", "..F..", "....."],
                "start": [1, 1],
                "goal": [1, 4],
            }
        )
        standing = Block(1, 2)
        self.assertFalse(board.is_valid_block(standing))
        lying = Block(1, 0)
        lying.move("RIGHT")
        self.assertEqual(lying.orientation, Orientation.HORIZONTAL)
        self.assertTrue(board.is_valid_block(lying))

    def test_soft_switch_opens_bridge_when_any_part_presses_it(self):
        board = Board(Path(__file__).parents[1] / "maps" / "level4.json")
        result = board.transition(Block(*board.start), board.initial_bridge_states, "RIGHT")
        self.assertTrue(result.valid)
        self.assertIn("soft_toggle", result.activated_switches)
        self.assertTrue(dict(result.bridge_states)["soft_bridge"])

    def test_heavy_switch_requires_standing(self):
        board = Board(Path(__file__).parents[1] / "maps" / "level5.json")
        first = board.transition(Block(*board.start), board.initial_bridge_states, "RIGHT")
        self.assertFalse(dict(first.bridge_states)["heavy_bridge"])
        second = board.transition(first.block, first.bridge_states, "RIGHT")
        self.assertTrue(second.valid)
        self.assertTrue(dict(second.bridge_states)["heavy_bridge"])

    def test_split_switch_teleports_and_cubes_rejoin(self):
        board = Board(Path(__file__).parents[1] / "maps" / "level6.json")
        first = board.transition(Block(*board.start), board.initial_bridge_states, "RIGHT")
        second = board.transition(first.block, first.bridge_states, "RIGHT")
        self.assertTrue(second.block.is_split)
        self.assertEqual(second.block.get_cells(), [(1, 1), (1, 4)])

        third = board.transition(second.block, second.bridge_states, "RIGHT")
        fourth = board.transition(third.block, third.bridge_states, "RIGHT")
        self.assertEqual(fourth.block.orientation, Orientation.HORIZONTAL)


if __name__ == "__main__":
    unittest.main()
