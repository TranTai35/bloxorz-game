import heapq
from itertools import count

from algorithms.metrics import SearchMetrics
from algorithms.successor import get_successors
from state import State


def ucs(board, start_block, start_bridge_states=None):
    metrics = SearchMetrics()
    root = State(
        start_block.copy(),
        board.normalize_bridge_states(start_bridge_states),
    )
    order = count()
    frontier = [(0.0, next(order), root)]
    best_cost = {root.key(): 0.0}
    expanded_nodes = 0
    generated_nodes = 1
    peak_frontier = 1

    while frontier:
        cost, _, current = heapq.heappop(frontier)
        if cost > best_cost.get(current.key(), float("inf")):
            continue
        expanded_nodes += 1

        if board.is_win(current.block):
            return metrics.result(
                goal_state=current,
                expanded_nodes=expanded_nodes,
                generated_nodes=generated_nodes,
                peak_frontier=peak_frontier,
            )

        successors = get_successors(current, board)
        generated_nodes += len(successors)
        for successor in successors:
            key = successor.key()
            if successor.cost >= best_cost.get(key, float("inf")):
                continue
            best_cost[key] = successor.cost
            heapq.heappush(frontier, (successor.cost, next(order), successor))
        peak_frontier = max(peak_frontier, len(frontier))

    return metrics.result(
        expanded_nodes=expanded_nodes,
        generated_nodes=generated_nodes,
        peak_frontier=peak_frontier,
    )
