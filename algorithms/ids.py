import sys

from algorithms.metrics import SearchMetrics
from algorithms.successor import get_successors
from state import State


def ids(board, start_block, start_bridge_states=None, max_depth=None):
    """Iterative Deepening Search with cycle and repeated-state pruning."""
    metrics = SearchMetrics()
    root = State(
        start_block.copy(),
        board.normalize_bridge_states(start_bridge_states),
    )
    if max_depth is None:
        max_depth = board.estimated_state_count()
    sys.setrecursionlimit(max(sys.getrecursionlimit(), min(max_depth + 100, 100000)))

    expanded_nodes = 0
    generated_nodes = 0
    peak_frontier = 1

    def depth_limited(state, depth, limit, path_keys, best_depth):
        nonlocal expanded_nodes, generated_nodes, peak_frontier
        expanded_nodes += 1
        if board.is_win(state.block):
            return state, False

        successors = get_successors(state, board)
        generated_nodes += len(successors)
        if depth == limit:
            cutoff = any(successor.key() not in path_keys for successor in successors)
            return None, cutoff

        cutoff_occurred = False
        for successor in successors:
            key = successor.key()
            next_depth = depth + 1
            if key in path_keys:
                continue
            previous_depth = best_depth.get(key)
            if previous_depth is not None and previous_depth <= next_depth:
                continue

            best_depth[key] = next_depth
            path_keys.add(key)
            peak_frontier = max(peak_frontier, len(path_keys))
            found, cutoff = depth_limited(
                successor,
                next_depth,
                limit,
                path_keys,
                best_depth,
            )
            path_keys.remove(key)
            if found is not None:
                return found, False
            cutoff_occurred = cutoff_occurred or cutoff

        return None, cutoff_occurred

    for depth_limit in range(max_depth + 1):
        generated_nodes += 1
        root_key = root.key()
        goal, cutoff = depth_limited(
            root,
            0,
            depth_limit,
            {root_key},
            {root_key: 0},
        )
        if goal is not None:
            return metrics.result(
                goal_state=goal,
                expanded_nodes=expanded_nodes,
                generated_nodes=generated_nodes,
                peak_frontier=peak_frontier,
            )
        if not cutoff:
            break

    return metrics.result(
        expanded_nodes=expanded_nodes,
        generated_nodes=generated_nodes,
        peak_frontier=peak_frontier,
    )
