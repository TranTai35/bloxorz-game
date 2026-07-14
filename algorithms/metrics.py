import time
import tracemalloc

from algorithms.search_result import SearchResult


class SearchMetrics:
    def __init__(self):
        self.started_tracing = not tracemalloc.is_tracing()
        if self.started_tracing:
            tracemalloc.start()
        tracemalloc.reset_peak()
        self.start_time = time.perf_counter()

    def result(
        self,
        *,
        goal_state=None,
        expanded_nodes=0,
        generated_nodes=0,
        peak_frontier=0,
    ):
        search_time = time.perf_counter() - self.start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        if self.started_tracing:
            tracemalloc.stop()

        found = goal_state is not None
        return SearchResult(
            path=goal_state.get_path() if found else [],
            expanded_nodes=expanded_nodes,
            generated_nodes=generated_nodes,
            peak_frontier=peak_frontier,
            search_time=search_time,
            memory_usage=peak_memory,
            solution_cost=goal_state.cost if found else 0.0,
            found=found,
        )
