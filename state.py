class State:
    def __init__(
        self,
        block,
        bridge_states=(),
        parent=None,
        action=None,
        cost=0.0,
    ):
        self.block = block
        self.bridge_states = tuple(bridge_states)
        self.parent = parent
        self.action = action
        self.cost = float(cost)

    def copy(self):
        return State(
            self.block.copy(),
            self.bridge_states,
            self.parent,
            self.action,
            self.cost,
        )

    def get_path(self):
        path = []
        current = self
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
        path.reverse()
        return path

    def key(self):
        return self.block.state_key(), self.bridge_states

    def __eq__(self, other):
        return isinstance(other, State) and self.key() == other.key()

    def __hash__(self):
        return hash(self.key())

    def __str__(self):
        return (
            f"{self.block} | Bridges={dict(self.bridge_states)} | "
            f"Cost={self.cost:.2f}"
        )
