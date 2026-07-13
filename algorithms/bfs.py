from collections import deque
from state import State
from .successor import get_successors


def bfs(board, start_block):
    """
    Tìm đường đi bằng Breadth-First Search (BFS)

    Parameters
    ----------
    board : Board
    start_block : Block

    Returns
    -------
    State hoặc None
    """

    # Tạo trạng thái ban đầu
    start_state = State(start_block)

    # Queue của BFS
    queue = deque()
    queue.append(start_state)

    # Tập trạng thái đã duyệt
    visited = set()
    visited.add(start_state)

    while queue:

        # Lấy state đầu tiên
        current_state = queue.popleft()

        # Kiểm tra đã tới Goal chưa
        if board.is_win(current_state.block):
            return current_state

        # Sinh các trạng thái mới
        successors = get_successors(current_state, board)

        for next_state in successors:

            if next_state not in visited:

                visited.add(next_state)
                queue.append(next_state)

    return None