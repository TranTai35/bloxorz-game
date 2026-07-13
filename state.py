from block import Block


class State:
    def __init__(self, block, parent=None, action=None, cost=0):
        """
        block   : Trạng thái hiện tại của block.
        parent  : State trước đó (dùng để truy vết lời giải).
        action  : Hành động dẫn tới state này (UP, DOWN, LEFT, RIGHT).
        cost    : Chi phí từ trạng thái đầu đến state này.
        """

        self.block = block
        self.parent = parent
        self.action = action
        self.cost = cost

    def copy(self):
        return State(
            self.block.copy(),
            self.parent,
            self.action,
            self.cost
        )

    def get_path(self):
        """
        Trả về danh sách các bước đi từ Start đến Goal.
        """

        path = []

        current = self

        while current.parent is not None:
            path.append(current.action)
            current = current.parent

        path.reverse()

        return path

    def __eq__(self, other):
        return (
            self.block.orientation == other.block.orientation
            and self.block.pos1 == other.block.pos1
            and self.block.pos2 == other.block.pos2
        )

    def __hash__(self):
        return hash((
            self.block.orientation,
            self.block.pos1,
            self.block.pos2
        ))

    def __str__(self):
        return (
            f"{self.block.orientation.name} | "
            f"{self.block.pos1} | "
            f"{self.block.pos2} | "
            f"Cost = {self.cost}"
        )