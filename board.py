import json
from block import Orientation


class Board:
    def __init__(self, filename):

        with open(filename, "r") as f:
            data = json.load(f)

        self.grid = [list(row) for row in data["grid"]]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.start = tuple(data["start"])
        self.goal = tuple(data["goal"])

    def is_inside(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_void(self, row, col):
        if not self.is_inside(row, col):
            return True

        return self.grid[row][col] == "#"

    def is_floor(self, row, col):
        if not self.is_inside(row, col):
            return False

        return self.grid[row][col] != "#"

    def is_goal(self, row, col):
        return (row, col) == self.goal

    def is_valid_block(self, block):

        for row, col in block.get_cells():

            if not self.is_inside(row, col):
                return False

            if self.is_void(row, col):
                return False

        return True

    def is_win(self, block):

        if block.orientation != Orientation.STANDING:
            return False

        return block.pos1 == self.goal

    def print_board(self):

        for row in self.grid:
            print(" ".join(row))