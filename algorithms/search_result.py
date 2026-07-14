class SearchResult:
    def __init__(
        self,
        path=None,
        expanded_nodes=0,
        generated_nodes=0,
        peak_frontier=0,
        search_time=0.0,
        memory_usage=0,
        solution_cost=0.0,
        found=False,
    ):
        self.path = path if path is not None else []
        self.steps = len(self.path)
        self.expanded_nodes = expanded_nodes
        self.generated_nodes = generated_nodes
        self.peak_frontier = peak_frontier
        self.search_time = search_time
        self.memory_usage = memory_usage
        self.solution_cost = solution_cost
        self.found = found

    @property
    def memory_usage_mb(self):
        return self.memory_usage / (1024 * 1024)

    def __str__(self):
        return (
            f"Found: {self.found}\n"
            f"Path: {self.path}\n"
            f"Steps: {self.steps}\n"
            f"Solution cost: {self.solution_cost:.2f}\n"
            f"Expanded nodes: {self.expanded_nodes}\n"
            f"Generated nodes: {self.generated_nodes}\n"
            f"Peak frontier: {self.peak_frontier}\n"
            f"Peak memory: {self.memory_usage_mb:.3f} MB\n"
            f"Search time: {self.search_time:.6f}s"
        )
