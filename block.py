from enum import Enum


class Orientation(Enum):
    STANDING = 0
    HORIZONTAL = 1
    VERTICAL = 2
    SPLIT = 3


class Block:
    """Pure-Python representation of the Bloxorz block.

    In split mode ``pos1`` and ``pos2`` are the two unit cubes and
    ``active_index`` identifies the cube controlled by the arrow/WASD keys.
    """

    def __init__(self, row, col):
        self.pos1 = (row, col)
        self.pos2 = (row, col)
        self.orientation = Orientation.STANDING
        self.active_index = 0

    @classmethod
    def split(cls, pos1, pos2, active_index=0):
        block = cls(*pos1)
        block.pos1 = tuple(pos1)
        block.pos2 = tuple(pos2)
        block.orientation = Orientation.SPLIT
        block.active_index = 0 if active_index not in (0, 1) else active_index
        return block

    @property
    def is_split(self):
        return self.orientation == Orientation.SPLIT

    def copy(self):
        new_block = Block(0, 0)
        new_block.pos1 = self.pos1
        new_block.pos2 = self.pos2
        new_block.orientation = self.orientation
        new_block.active_index = self.active_index
        return new_block

    def get_cells(self):
        if self.orientation == Orientation.STANDING:
            return [self.pos1]
        return [self.pos1, self.pos2]

    def get_active_cell(self):
        if not self.is_split:
            raise ValueError("Khối chưa ở trạng thái tách")
        return self.pos1 if self.active_index == 0 else self.pos2

    def state_key(self):
        return (
            self.orientation.value,
            self.pos1,
            self.pos2,
            self.active_index if self.is_split else 0,
        )

    def _move_split_cube(self, row_delta, col_delta):
        if self.active_index == 0:
            row, col = self.pos1
            self.pos1 = (row + row_delta, col + col_delta)
        else:
            row, col = self.pos2
            self.pos2 = (row + row_delta, col + col_delta)
        self._merge_if_adjacent()

    def _merge_if_adjacent(self):
        row1, col1 = self.pos1
        row2, col2 = self.pos2

        if row1 == row2 and abs(col1 - col2) == 1:
            left, right = sorted((self.pos1, self.pos2), key=lambda cell: cell[1])
            self.pos1, self.pos2 = left, right
            self.orientation = Orientation.HORIZONTAL
            self.active_index = 0
        elif col1 == col2 and abs(row1 - row2) == 1:
            top, bottom = sorted((self.pos1, self.pos2), key=lambda cell: cell[0])
            self.pos1, self.pos2 = top, bottom
            self.orientation = Orientation.VERTICAL
            self.active_index = 0

    def switch_active_cube(self):
        if not self.is_split:
            raise ValueError("Chỉ có thể đổi điều khiển khi khối đã tách")
        self.active_index = 1 - self.active_index

    def move_up(self):
        if self.is_split:
            self._move_split_cube(-1, 0)
            return

        row1, col1 = self.pos1
        if self.orientation == Orientation.STANDING:
            self.pos1 = (row1 - 2, col1)
            self.pos2 = (row1 - 1, col1)
            self.orientation = Orientation.VERTICAL
        elif self.orientation == Orientation.VERTICAL:
            self.pos1 = (row1 - 1, col1)
            self.pos2 = self.pos1
            self.orientation = Orientation.STANDING
        else:
            row2, col2 = self.pos2
            self.pos1 = (row1 - 1, col1)
            self.pos2 = (row2 - 1, col2)

    def move_down(self):
        if self.is_split:
            self._move_split_cube(1, 0)
            return

        row1, col1 = self.pos1
        if self.orientation == Orientation.STANDING:
            self.pos1 = (row1 + 1, col1)
            self.pos2 = (row1 + 2, col1)
            self.orientation = Orientation.VERTICAL
        elif self.orientation == Orientation.VERTICAL:
            row2, col2 = self.pos2
            self.pos1 = (row2 + 1, col2)
            self.pos2 = self.pos1
            self.orientation = Orientation.STANDING
        else:
            row2, col2 = self.pos2
            self.pos1 = (row1 + 1, col1)
            self.pos2 = (row2 + 1, col2)

    def move_left(self):
        if self.is_split:
            self._move_split_cube(0, -1)
            return

        row1, col1 = self.pos1
        if self.orientation == Orientation.STANDING:
            self.pos1 = (row1, col1 - 2)
            self.pos2 = (row1, col1 - 1)
            self.orientation = Orientation.HORIZONTAL
        elif self.orientation == Orientation.HORIZONTAL:
            self.pos1 = (row1, col1 - 1)
            self.pos2 = self.pos1
            self.orientation = Orientation.STANDING
        else:
            row2, col2 = self.pos2
            self.pos1 = (row1, col1 - 1)
            self.pos2 = (row2, col2 - 1)

    def move_right(self):
        if self.is_split:
            self._move_split_cube(0, 1)
            return

        row1, col1 = self.pos1
        if self.orientation == Orientation.STANDING:
            self.pos1 = (row1, col1 + 1)
            self.pos2 = (row1, col1 + 2)
            self.orientation = Orientation.HORIZONTAL
        elif self.orientation == Orientation.HORIZONTAL:
            row2, col2 = self.pos2
            self.pos1 = (row2, col2 + 1)
            self.pos2 = self.pos1
            self.orientation = Orientation.STANDING
        else:
            row2, col2 = self.pos2
            self.pos1 = (row1, col1 + 1)
            self.pos2 = (row2, col2 + 1)

    def move(self, direction):
        direction = direction.upper()
        handlers = {
            "UP": self.move_up,
            "DOWN": self.move_down,
            "LEFT": self.move_left,
            "RIGHT": self.move_right,
            "SWITCH": self.switch_active_cube,
        }
        try:
            handlers[direction]()
        except KeyError as error:
            raise ValueError(f"Hướng không hợp lệ: {direction}") from error
        return self

    def __str__(self):
        active = f" | active={self.active_index + 1}" if self.is_split else ""
        return f"{self.orientation.name} | {self.pos1} | {self.pos2}{active}"
