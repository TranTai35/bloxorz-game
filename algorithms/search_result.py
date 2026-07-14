class SearchResult:
    def __init__(
        self,
        path=None,
        expanded_nodes=0,
        search_time=0.0,
        found=False
    ):
        self.path = path if path is not None else []
        self.steps = len(self.path)
        self.expanded_nodes = expanded_nodes
        self.search_time = search_time
        self.found = found

    def __str__(self):
        return (
            f"Found: {self.found}\n"
            f"Path: {self.path}\n"
            f"Steps: {self.steps}\n"
            f"Expanded nodes: {self.expanded_nodes}\n"
            f"Search time: {self.search_time:.6f}s"
        )