import unittest
from pathlib import Path

from algorithms.solver import solve
from block import Block
from board import Board


class SolverTests(unittest.TestCase):
    def replay(self, board, path):
        block = Block(*board.start)
        bridge_states = board.initial_bridge_states
        for action in path:
            result = board.transition(block, bridge_states, action)
            self.assertTrue(result.valid, f"Lời giải có bước không hợp lệ: {action}")
            block = result.block
            bridge_states = result.bridge_states
        return block

    def test_all_algorithms_solve_basic_and_advanced_levels(self):
        maps_dir = Path(__file__).parents[1] / "maps"
        for level_name in (
            "level1.json",
            "level4.json",
            "level5.json",
            "level6.json",
            "level7.json",
        ):
            for algorithm in ("BFS", "IDS", "UCS", "ASTAR"):
                with self.subTest(level=level_name, algorithm=algorithm):
                    board = Board(maps_dir / level_name)
                    result = solve(board, Block(*board.start), algorithm)
                    self.assertTrue(result.found)
                    self.assertTrue(board.is_win(self.replay(board, result.path)))
                    self.assertEqual(result.steps, len(result.path))
                    self.assertGreater(result.expanded_nodes, 0)
                    self.assertGreater(result.generated_nodes, 0)
                    self.assertGreaterEqual(result.memory_usage, 0)

    def test_solver_can_change_the_active_split_cube(self):
        board = Board(Path(__file__).parents[1] / "maps" / "level7.json")
        result = solve(board, Block(*board.start), "ASTAR")
        self.assertTrue(result.found)
        self.assertIn("SWITCH", result.path)
        self.assertTrue(board.is_win(self.replay(board, result.path)))

    def test_ucs_uses_non_uniform_cost(self):
        board = Board(Path(__file__).parents[1] / "maps" / "level3.json")
        bfs_result = solve(board, Block(*board.start), "BFS")
        ucs_result = solve(board, Block(*board.start), "UCS")
        self.assertEqual(bfs_result.steps, ucs_result.steps)
        self.assertLess(ucs_result.solution_cost, bfs_result.solution_cost)


if __name__ == "__main__":
    unittest.main()
