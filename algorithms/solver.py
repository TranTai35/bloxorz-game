from algorithms.bfs import bfs

# Sau này import thêm:
# from algorithms.ids import ids
# from algorithms.ucs import ucs
# from algorithms.astar import astar


def solve(board, start_block, algorithm_name):
    algorithm_name = algorithm_name.upper()

    if algorithm_name == "BFS":
        return bfs(board, start_block)

    # Sau này mở dần:
    # if algorithm_name == "DFS":
    #     return dfs(board, start_block)

    # if algorithm_name == "UCS":
    #     return ucs(board, start_block)

    # if algorithm_name == "ASTAR":
    #     return astar(board, start_block)

    raise ValueError(
        f"Thuật toán không hợp lệ: {algorithm_name}"
    )