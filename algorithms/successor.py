from state import State


def get_successors(state, board):
    """
    Sinh tất cả trạng thái kế tiếp hợp lệ từ state hiện tại.
    """

    successors = []

    directions = ["UP", "DOWN", "LEFT", "RIGHT"]

    for direction in directions:

        # Copy block hiện tại
        new_block = state.block.copy()

        # Di chuyển
        new_block.move(direction)

        # Kiểm tra hợp lệ
        if board.is_valid_block(new_block):

            new_state = State(
                block=new_block,
                parent=state,
                action=direction,
                cost=state.cost + 1
            )

            successors.append(new_state)

    return successors