from enum import Enum


class Orientation(Enum):
    STANDING = 0
    HORIZONTAL = 1
    VERTICAL = 2


class Block:
    def __init__(self, row, col):
        self.pos1 = (row, col)
        self.pos2 = (row, col)
        self.orientation = Orientation.STANDING

    def copy(self):
        new_block = Block(0, 0)
        new_block.pos1 = self.pos1
        new_block.pos2 = self.pos2
        new_block.orientation = self.orientation
        return new_block

    def get_cells(self):
        return [self.pos1, self.pos2]

    def move_up(self):
        r1, c1 = self.pos1

        if self.orientation == Orientation.STANDING:
            self.pos1 = (r1 - 2, c1)
            self.pos2 = (r1 - 1, c1)
            self.orientation = Orientation.VERTICAL

        elif self.orientation == Orientation.VERTICAL:
            self.pos1 = (r1 - 1, c1)
            self.pos2 = (r1 - 1, c1)
            self.orientation = Orientation.STANDING

        elif self.orientation == Orientation.HORIZONTAL:
            r2, c2 = self.pos2
            self.pos1 = (r1 - 1, c1)
            self.pos2 = (r2 - 1, c2)

    def move_down(self):
        r1, c1 = self.pos1

        if self.orientation == Orientation.STANDING:
            self.pos1 = (r1 + 1, c1)
            self.pos2 = (r1 + 2, c1)
            self.orientation = Orientation.VERTICAL

        elif self.orientation == Orientation.VERTICAL:
            r2, c2 = self.pos2
            self.pos1 = (r2 + 1, c2)
            self.pos2 = (r2 + 1, c2)
            self.orientation = Orientation.STANDING

        elif self.orientation == Orientation.HORIZONTAL:
            r2, c2 = self.pos2
            self.pos1 = (r1 + 1, c1)
            self.pos2 = (r2 + 1, c2)

    def move_left(self):
        r1, c1 = self.pos1

        if self.orientation == Orientation.STANDING:
            self.pos1 = (r1, c1 - 2)
            self.pos2 = (r1, c1 - 1)
            self.orientation = Orientation.HORIZONTAL

        elif self.orientation == Orientation.HORIZONTAL:
            self.pos1 = (r1, c1 - 1)
            self.pos2 = (r1, c1 - 1)
            self.orientation = Orientation.STANDING

        elif self.orientation == Orientation.VERTICAL:
            r2, c2 = self.pos2
            self.pos1 = (r1, c1 - 1)
            self.pos2 = (r2, c2 - 1)

    def move_right(self):
        r1, c1 = self.pos1

        if self.orientation == Orientation.STANDING:
            self.pos1 = (r1, c1 + 1)
            self.pos2 = (r1, c1 + 2)
            self.orientation = Orientation.HORIZONTAL

        elif self.orientation == Orientation.HORIZONTAL:
            r2, c2 = self.pos2
            self.pos1 = (r2, c2 + 1)
            self.pos2 = (r2, c2 + 1)
            self.orientation = Orientation.STANDING

        elif self.orientation == Orientation.VERTICAL:
            r2, c2 = self.pos2
            self.pos1 = (r1, c1 + 1)
            self.pos2 = (r2, c2 + 1)

    def move(self, direction):
        direction = direction.upper()

        if direction == "UP":
            self.move_up()
        elif direction == "DOWN":
            self.move_down()
        elif direction == "LEFT":
            self.move_left()
        elif direction == "RIGHT":
            self.move_right()
        else:
            raise ValueError("Invalid direction")

    def __str__(self):
        return f"{self.orientation.name} | {self.pos1} | {self.pos2}"


if __name__ == "__main__":
    block = Block(3, 3)

    print(block)

    block.move("UP")
    print(block)

    block.move("RIGHT")
    print(block)

    block.move("DOWN")
    print(block)

    block.move("LEFT")
    print(block)