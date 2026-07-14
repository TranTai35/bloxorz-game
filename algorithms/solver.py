from algorithms.astar import astar
from algorithms.bfs import bfs
from algorithms.ids import ids
from algorithms.ucs import ucs


def solve(board, start_block, algorithm_name, start_bridge_states=None):
    normalized_name = algorithm_name.upper().replace("*", "STAR")
    algorithms = {
        "BFS": bfs,
        "DFS": ids,  # The assignment explicitly permits IDS instead of DFS.
        "IDS": ids,
        "UCS": ucs,
        "ASTAR": astar,
    }
    try:
        algorithm = algorithms[normalized_name]
    except KeyError as error:
        raise ValueError(f"Thuật toán không hợp lệ: {algorithm_name}") from error
    return algorithm(board, start_block, start_bridge_states)
