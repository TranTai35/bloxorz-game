from state import State


def get_successors(state, board):
    """Generate every valid successor using the same rules as manual play."""
    successors = []
    for action in board.available_actions(state.block):
        result = board.transition(state.block, state.bridge_states, action)
        if not result.valid:
            continue
        successors.append(
            State(
                block=result.block,
                bridge_states=result.bridge_states,
                parent=state,
                action=action,
                cost=state.cost + board.get_action_cost(result, action),
            )
        )
    return successors
