import time
from collections import deque

from state import State
from algorithms.successor import get_successors
from algorithms.search_result import SearchResult


def bfs(board, start_block):
    search_start = time.perf_counter()

    start_state = State(start_block)

    queue = deque([start_state])
    visited = {start_state}

    expanded_nodes = 0

    while queue:
        current_state = queue.popleft()

        expanded_nodes += 1

        if board.is_win(current_state.block):
            search_time = time.perf_counter() - search_start

            path = current_state.get_path()

            return SearchResult(
                path=path,
                expanded_nodes=expanded_nodes,
                search_time=search_time,
                found=True
            )

        for next_state in get_successors(current_state, board):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)

    search_time = time.perf_counter() - search_start

    return SearchResult(
        path=[],
        expanded_nodes=expanded_nodes,
        search_time=search_time,
        found=False
    )